from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from common.db_utils import get_db_connection
from psycopg2.extras import RealDictCursor

def user_profile(request):
    if request.method == 'GET':
        try:
            # Get session user_id
            user_id = request.session.get('user_id')
            if not user_id:
                return JsonResponse({'error': 'User not logged in'}, status=403)

            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            # Query the User table for user details
            cursor.execute(
                """
                SELECT name, role, email_id, password_hashed, skills, preferences, last_login 
                FROM "User" WHERE user_id = %s
                """,
                (user_id,)
            )
            user = cursor.fetchone()

            if not user:
                return JsonResponse({'error': 'User not found'}, status=404)

            # Query the Project_Team table to find user's projects and roles
            cursor.execute(
                """
                SELECT pt.role_in_project, p.project_name, p.project_id 
                FROM "Project_Team" pt
                JOIN "Project" p ON pt.project_id = p.project_id
                WHERE pt.user_id = %s
                """,
                (user_id,)
            )
            project_details = cursor.fetchall()

            # Query the Task table to find user's assigned tasks
            cursor.execute(
                """
                SELECT task_id, task_name, description, status, due_date, project_id 
                FROM "Task" WHERE assigned_user_id = %s
                """,
                (user_id,)
            )
            assigned_tasks = cursor.fetchall()

            # Close the connection
            cursor.close()
            conn.close()

            # Build the response
            response = {
                'user': user,
                'projects': project_details,
                'tasks': assigned_tasks
            }

            return JsonResponse(response, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
@csrf_exempt
def list_projects(request):
    if request.method == 'GET':
        try:
            user_role = request.session.get('role')  # Assuming role is stored in the session
            user_id = request.session.get('user_id')  # Assuming user_id is stored in the session

            if not user_role or not user_id:
                return JsonResponse({'error': 'Unauthorized access. Please log in.'}, status=403)

            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            if user_role == 'Manager':
                # Managers can only see projects where they are the manager
                cursor.execute("""
                    SELECT * FROM "Project" 
                    WHERE manager_id = %s
                """, (user_id,))
            else:
                # Employees can only see projects they are assigned to in the Project_Team table
                cursor.execute("""
                    SELECT p.* 
                    FROM "Project" p
                    INNER JOIN "Project_Team" pt ON p.project_id = pt.project_id
                    WHERE pt.user_id = %s
                """, (user_id,))

            projects = cursor.fetchall()
            cursor.close()
            conn.close()

            return JsonResponse({'projects': projects}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def project_detail(request, project_id):
    user_role = request.session.get('role')  # Assuming role is stored in the session
    user_id = request.session.get('user_id')  # Assuming user_id is stored in the session
    request.session['project_id'] = project_id
    if request.method == 'GET':
        try:
            # user_role = request.session.get('role')  # Assuming role is stored in the session
            # user_id = request.session.get('user_id')  # Assuming user_id is stored in the session
            # request.session['project_id'] = project_id
            if not user_role or not user_id:
                return JsonResponse({'error': 'Unauthorized access. Please log in.'}, status=403)

            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            if user_role == 'Manager':
                # Managers can only view details of projects they manage
                cursor.execute("""
                    SELECT * FROM "Project" 
                    WHERE project_id = %s AND manager_id = %s
                """, (project_id, user_id))
            else:
                # Employees can only view details of projects they are part of in Project_Team
                cursor.execute("""
                    SELECT p.* 
                    FROM "Project" p
                    INNER JOIN "Project_Team" pt ON p.project_id = pt.project_id
                    WHERE p.project_id = %s AND pt.user_id = %s
                """, (project_id, user_id))

            project = cursor.fetchone()
            cursor.close()
            conn.close()

            if project:
                return JsonResponse({'project': project}, status=200)
            else:
                return JsonResponse({'error': 'Project not found or access denied'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
