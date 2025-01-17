from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from common.db_utils import get_db_connection
from psycopg2.extras import RealDictCursor
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from common.db_utils import get_db_connection
from psycopg2.extras import RealDictCursor

@csrf_exempt
def view_budget(request):
    
    if request.method == 'GET':
        try:
            user_role = request.session.get('role')
            user_id = request.session.get('user_id')
            project_id = request.session.get('project_id')
            # Check if the user role is 'Manager'
            if user_role == 'Manager':

                if not project_id:
                    return JsonResponse({'error': 'Project ID not found in session'}, status=400)

                # Connect to the database
                conn = get_db_connection()
                cursor = conn.cursor(cursor_factory=RealDictCursor)

                # Fetch the budget for the project_id from the session
                cursor.execute('SELECT * FROM "Budget" WHERE project_id = %s', (project_id,))

                budget = cursor.fetchone()
                cursor.close()
                conn.close()

                if budget:
                    return JsonResponse({'budget': budget}, status=200)
                else:
                    return JsonResponse({'error': 'No budget found for this project'}, status=404)
            else:
                return JsonResponse({'error': 'You are not authorized to view the budget'}, status=403)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
