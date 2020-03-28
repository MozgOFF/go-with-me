from rest_framework import serializers
from .models import Comment, User


class CommentAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']


class CommentChildSerializer(serializers.ModelSerializer):
    author = CommentAuthorSerializer()

    class Meta:
        model = Comment
        fields = ['content', 'author', 'created']


class CommentSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    author = CommentAuthorSerializer()

    class Meta:
        model = Comment
        fields = ['content', 'author', 'created', 'children']

    def get_children(self, obj):
        comments_qs = Comment.objects.filter(parent=obj)
        comments = CommentChildSerializer(comments_qs, many=True).data
        return comments


class CreateCommentSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ['content', 'event', 'author', 'parent']

    def create(self, validated_data):
        content = validated_data['content']
        event = validated_data['event']
        parent = validated_data.get('parent')
        author = validated_data['author']

        if parent is not None:
            parentInstance = Comment.objects.get(id=parent.id)
            if parentInstance.parent is not None:
                parent = parentInstance.parent

        comment = Comment(content=content, event=event, parent=parent, author=author)
        comment.save()

        return comment
