from django.db import models

# Create your models here.
class Board(models.Model):
    title       = models.CharField(max_length=200, verbose_name="제목")
    contents    = models.TextField(verbose_name="내용")
    writer      = models.ForeignKey('account.BoardMember', on_delete=models.CASCADE, verbose_name="작성자")
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    updated_at  = models.DateTimeField(auto_now=True, verbose_name="최종수정일")

    def __str__(self):
        return self.title

    class Meta:
        db_table            = 'boards'
        verbose_name        = '게시판'
        verbose_name_plural = '게시판'

class Comment(models.Model):
    board         = models.ForeignKey(Board, on_delete=models.CASCADE, null=True)
    contents      = models.TextField()
    created_at    = models.DateTimeField(auto_now_add=True)
    writer = models.ForeignKey('account.BoardMember', on_delete=models.CASCADE, verbose_name="댓글작성자")