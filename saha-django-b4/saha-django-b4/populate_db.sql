-- Populate User table
INSERT INTO "User" (user_id, name, email_id, password_hashed, role, skills, preferences, last_login) VALUES
(1, 'Amit Sharma', 'amit.sharma@example.com', 'hashed_password1', 'Manager', 'Leadership, Planning', 'Management', NOW()),
(2, 'Priya Gupta', 'priya.gupta@example.com', 'hashed_password2', 'Employee', 'Python, Django', 'Backend', NOW()),
(3, 'Rajesh Kumar', 'rajesh.kumar@example.com', 'hashed_password3', 'Employee', 'JavaScript, React', 'Frontend', NOW()),
(4, 'Neha Singh', 'neha.singh@example.com', 'hashed_password4', 'Manager', 'Budgeting, Coordination', 'Management', NOW()),
(5, 'Anjali Verma', 'anjali.verma@example.com', 'hashed_password5', 'Employee', 'SQL, Database Design', 'Backend', NOW()),
(6, 'Vikram Iyer', 'vikram.iyer@example.com', 'hashed_password6', 'Employee', 'Testing, Automation', 'Backend', NOW()),
(7, 'Ritu Das', 'ritu.das@example.com', 'hashed_password7', 'Employee', 'UI/UX Design', 'Frontend', NOW()),
(8, 'Suresh Nair', 'suresh.nair@example.com', 'hashed_password8', 'Manager', 'Risk Management', 'Management', NOW()),
(9, 'Meena Reddy', 'meena.reddy@example.com', 'hashed_password9', 'Employee', 'DevOps, CI/CD', 'Backend', NOW()),
(10, 'Arjun Patel', 'arjun.patel@example.com', 'hashed_password10', 'Employee', 'Machine Learning', 'Backend', NOW());

-- Populate Project table
INSERT INTO "Project" (project_id, project_name, description, start_date, end_date, completed, manager_id) VALUES
(1, 'Project Alpha', 'First project led by Amit Sharma', '2024-01-01', '2024-06-01', FALSE, 1),
(2, 'Project Beta', 'Second project led by Neha Singh', '2024-02-01', '2024-07-01', FALSE, 4),
(3, 'Project Gamma', 'Third project led by Suresh Nair', '2024-03-01', '2024-08-01', FALSE, 8),
(4, 'Project Delta', 'Fourth project with automation focus', '2024-04-01', '2024-09-01', FALSE, 1),
(5, 'Project Epsilon', 'Fifth project led by Neha Singh', '2024-05-01', '2024-10-01', FALSE, 4);

-- Populate Budget table
INSERT INTO "Budget" (budget_id, project_id, total_budget, remaining_budget, allocated_training, allocated_resources, allocated_salary) VALUES
(1, 1, 100000.00, 75000.00, 10000.00, 20000.00, 50000.00),
(2, 2, 200000.00, 150000.00, 20000.00, 30000.00, 100000.00),
(3, 3, 150000.00, 100000.00, 15000.00, 25000.00, 60000.00),
(4, 4, 120000.00, 90000.00, 10000.00, 20000.00, 60000.00),
(5, 5, 180000.00, 130000.00, 15000.00, 25000.00, 80000.00);

-- Populate Milestone table
INSERT INTO "Milestone" (milestone_id, project_id, deadline, end_state, status_milestone) VALUES
(1, 1, '2024-03-01', 'Phase 1 Complete', 'On Track'),
(2, 1, '2024-06-01', 'Phase 2 Complete', 'Pending'),
(3, 2, '2024-05-01', 'Documentation Done', 'On Track'),
(4, 2, '2024-07-01', 'Deployment', 'Pending'),
(5, 3, '2024-06-15', 'Initial Testing', 'On Track'),
(6, 3, '2024-08-01', 'Final Testing', 'Pending'),
(7, 4, '2024-05-01', 'Automation Tools Setup', 'On Track'),
(8, 4, '2024-09-01', 'Automation Complete', 'Pending'),
(9, 5, '2024-08-01', 'Phase 1 Review', 'On Track'),
(10, 5, '2024-10-01', 'Final Delivery', 'Pending');

-- Populate Task table
INSERT INTO "Task" (task_id, task_name, description, project_id, assigned_user_id, status, due_date) VALUES
(1, 'Setup Project Alpha', 'Initial setup for Project Alpha', 1, 2, 'In Progress', '2024-02-01'),
(2, 'Develop Core Features', 'Core features for Alpha', 1, 3, 'Pending', '2024-05-01'),
(3, 'Design Project Beta', 'Design initial phase of Beta', 2, 5, 'Pending', '2024-04-01'),
(4, 'Develop Beta Features', 'Develop core modules', 2, 6, 'Pending', '2024-06-01'),
(5, 'Setup Testing', 'Testing setup for Gamma', 3, 9, 'In Progress', '2024-05-01'),
(6, 'Final Review Gamma', 'Final review tasks', 3, 10, 'Pending', '2024-07-01'),
(7, 'Research Automation Tools', 'Automation tools research', 4, 6, 'In Progress', '2024-06-01'),
(8, 'Implement Automation', 'Implement automation framework', 4, 7, 'Pending', '2024-08-01'),
(9, 'Phase 1 Review', 'Phase 1 tasks for Epsilon', 5, 8, 'In Progress', '2024-07-01'),
(10, 'Delivery Prep Epsilon', 'Prepare for delivery', 5, 10, 'Pending', '2024-09-01');

-- Populate ProjectTeam table
INSERT INTO "Project_Team" (project_id, user_id, role_in_project) VALUES
(1, 2, 'Backend Developer'),
(1, 3, 'Frontend Developer'),
(2, 5, 'Database Designer'),
(2, 6, 'Backend Developer'),
(3, 9, 'DevOps Engineer'),
(3, 10, 'Reviewer'),
(4, 6, 'Tester'),
(4, 7, 'UI/UX Lead'),
(5, 8, 'Support Engineer'),
(5, 10, 'Analyst');

-- Populate StatusHistory table
INSERT INTO "Status_History" (task_id, changed_by, change_timestamp) VALUES
(1, 2, NOW()),
(2, 3, NOW()),
(3, 5, NOW()),
(4, 6, NOW()),
(5, 9, NOW()),
(6, 10, NOW());
