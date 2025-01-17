from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from common.db_utils import get_db_connection
from psycopg2.extras import RealDictCursor

@csrf_exempt
def create_task(request):
    if request.method == 'POST':
        try:
            user_role = request.session.get('role')  # Assuming role is stored in the session
            session_project_id = request.session.get('project_id')  # Project ID stored in session
            if user_role != 'Manager':
                return JsonResponse({'error': 'Permission denied. Only managers can create tasks.'}, status=403)
            import json
            data = json.loads(request.body)
            task_id = data.get('task_id')
            task_name = data.get('task_name')
            description = data.get('description')
            assigned_user = data.get('assigned_user_id')
            due_date = data.get('due_date')

            # Insert task into database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO "Task" (task_id, task_name, description, project_id, assigned_user_id, status, due_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (task_id, task_name, description, session_project_id, assigned_user, 'Pending', due_date))
            conn.commit()
            cursor.close()
            conn.close()

            return JsonResponse({'message': 'Task created successfully!'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def list_tasks(request):
    if request.method == 'GET':
        try:
            # Get role, user_id, and project_id from session
            user_role = request.session.get('role')  # 'manager' or 'employee'
            user_id = request.session.get('user_id')  # Logged-in user's ID
            session_project_id = request.session.get('project_id')  # Project ID stored in session

            if not user_role or not user_id or not session_project_id:
                return JsonResponse({'error': 'Unauthorized access. Please log in.'}, status=403)

            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            if user_role == 'Manager':
                # Managers: View tasks for the session's project_id
                cursor.execute("""
                    SELECT * FROM "Task" 
                    WHERE project_id = %s
                """, (session_project_id,))
            elif user_role == 'Employee':
                # Employees: View tasks for the session's project_id where they are the assigned user
                cursor.execute("""
                    SELECT * FROM "Task" 
                    WHERE project_id = %s AND assigned_user_id = %s
                """, (session_project_id, user_id))
            else:
                return JsonResponse({'error': 'Invalid user role.'}, status=403)

            tasks = cursor.fetchall()
            cursor.close()
            conn.close()

            return JsonResponse({'tasks': tasks}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)