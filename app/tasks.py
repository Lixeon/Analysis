import requests
from rq import get_current_job
from app import create_app

app = create_app()
app.app_context().push()



def _query_url_pass(url):
    resp = requests.get(url,timeout=2)
    code = resp.status_code
    return code
    
# def _set_task_progress(progress):
    
#     if job:
#         = progress
#         job.save_meta()
#         task = Task.query.get(job.get_id())
#         task.user.add_notification('task_progress', {'task_id': job.get_id(),
#                                                      'progress': progress})
#         if progress >= 100:
#             task.complete = True
#         db.session.commit()

def query_servers(ngroks):
    job = get_current_job()
    print('Starting task')
    for i in range(len(ngroks)):
        job.meta['progress'] = 100.0 * i / len(ngroks)
        job.save_meta()
        print(i)
        ngroks[i].status=_query_url_pass(ngroks[i].pub)
        db.session.commit()
        # time.sleep(1)
    job.meta['progress'] = 100
    job.save_meta()
    print('Task completed')
    return ngroks


# import sys
# # ...


# def export_posts(user_id):
#     try:
#         job = get_current_job()
#         job.meta['progress']=0
#         job.save_meta()
#         data = []
#         i = 0
#         total_servers = len(Ngrok.query.all())
#         for post in user.posts.order_by(Post.timestamp.asc()):
#             data.append({'body': post.body,
#                          'timestamp': post.timestamp.isoformat() + 'Z'})
#             time.sleep(5)
#             i += 1
#             _set_task_progress(100 * i // total_posts)
#     except:
#         _set_task_progress(100)
#         app.logger.error('Unhandled exception', exc_info=sys.exc_info())
