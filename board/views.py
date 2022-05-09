from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.http import Http404
from datetime import datetime
from account.models import BoardMember
from .models import Board, Comment
from .forms import BoardForm
# Create your views here.

def board_list(request):
    all_boards  = Board.objects.all().order_by('-id')
    # 변수명을 all_boards 로 바꿔주었다.
    page        = int(request.GET.get('p', 1))
    # p라는 값으로 받을거고, 없으면 첫번째 페이지로
    pagenator   = Paginator(all_boards, 5)
    # Paginator 함수를 적용하는데, 첫번째 인자는 위에 변수인 전체 오브젝트, 2번째 인자는
    # 한 페이지당 오브젝트 2개씩 나오게 설정
    boards      = pagenator.get_page(page) 
    return render(request, 'board/board_list.html', {"boards":boards})


def board_write(request):
    if not request.session.get('user'):
        return redirect('/account/login/')
    if request.method == "POST":
        form = BoardForm(request.POST)

        if form.is_valid():
            # form의 모든 validators 호출 유효성 검증 수행
            user_id = request.session.get('user')
            member = BoardMember.objects.get(pk=user_id)
            
            board = Board()
            board.title     = form.cleaned_data['title']
            board.contents  = form.cleaned_data['contents']
            board.writer    = member
            board.save()

            return redirect('/board/list/')

    else:
        form = BoardForm()

    return render(request, 'board/board_write.html', {'form': form})


def board_detail(request, pk):
    # 댓글 기능
    comment_count = Comment.objects.filter(board_id=pk).count()
    try:
        auth = False
        comment_auth = request.session.get('user')
        board_id = get_object_or_404(Board,pk=pk)
        board = Board.objects.get(pk=pk)
        comments = Comment.objects.filter(board=pk)
        if board.writer_id == request.session.get('user'):
            auth = True
    except Board.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다')
        # 게시물의 내용을 찾을 수 없을 때 내는 오류 message.
    
    # 댓글 쓰기
    if request.method == "POST":
        user_id = request.session.get('user')
        comment = Comment()
        member = BoardMember.objects.get(pk=user_id)
        comment.board    = board_id
        comment.contents = request.POST['contents']
        comment.writer = member
        comment.save()
        return redirect('.')
    return render(request, 'board/board_detail.html', {'board':board, 'auth':auth, 'comment_auth':comment_auth, 'comments':comments, 'comment_count':comment_count})


def board_update(request, pk):
    if not request.session.get('user'):
        return redirect('/account/login/')

    board = Board.objects.get(pk=pk)
    if board.writer_id == request.session.get('user'):
        if request.method == "POST":
            form = BoardForm(request.POST)
            board.title = request.POST['title']
            board.contents = request.POST['contents']
            board.updated_at = datetime.now()
            board.save()
            return redirect('/board/detail/%s' % pk)

        else:
            form = BoardForm()
    else:
        return redirect('/board/update/fail/')
    return render(request, 'board/board_update.html', {'form':form, 'board':board})

def board_update_fail(request):
    return render(request, 'board/board_update_fail.html')

def board_delete(request, pk):
    if not request.session.get('user'):
        return redirect('/account/login/')

    board = Board.objects.get(id=pk)
    if board.writer_id == request.session.get('user'):
        board.delete()
        return redirect('/board/list/')
    else:
        return redirect('/board/delete/fail')

def board_delete_fail(request):
    return render(request, 'board/board_delete_fail.html')

# def comment_detail(request, pk):
#   comment_detail = get_object_or_404(Board,pk=pk)
#   comments = Comment.objects.filter(board = pk)
#   if request.method == "POST":
#     comment = Comment()
#     comment.board = comment_detail
#     comment.contents = request.POST['contents']
#     comment.save()
#   return render(request,'detail.html',{'post':comment_detail, 'comments':comments})

def comment_delete(request, ck, pk):
    if not request.session.get('user'):
        return redirect('/account/login/')

    comment = Comment.objects.get(id=ck)
    if comment.writer_id == request.session.get('user'):
        comment.delete()
        return redirect('/board/detail/%s' % pk)
    else:
        return redirect('/board/delete/fail')