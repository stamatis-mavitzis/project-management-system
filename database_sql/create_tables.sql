
-- ============================================
-- Project Management System Database Schema
-- PostgreSQL SQL Script (Updated)
-- ============================================

-- ============================================
-- CLEANUP (Drop existing tables and types)
-- ============================================
DROP TABLE IF EXISTS attachments CASCADE;
DROP TABLE IF EXISTS comments CASCADE;
DROP TABLE IF EXISTS tasks CASCADE;
DROP TABLE IF EXISTS team_members CASCADE;
DROP TABLE IF EXISTS teams CASCADE;
DROP TABLE IF EXISTS users CASCADE;

DROP TYPE IF EXISTS task_priority CASCADE;
DROP TYPE IF EXISTS task_status CASCADE;
DROP TYPE IF EXISTS user_status CASCADE;
DROP TYPE IF EXISTS user_role CASCADE;

-- ============================================
-- ENUM Types
-- ============================================
CREATE TYPE user_role AS ENUM ('ADMIN', 'TEAM_LEADER', 'MEMBER');
CREATE TYPE user_status AS ENUM ('ACTIVE', 'INACTIVE', 'PENDING');
CREATE TYPE task_status AS ENUM ('TODO', 'IN_PROGRESS', 'DONE');
CREATE TYPE task_priority AS ENUM ('LOW', 'MEDIUM', 'HIGH');

-- ============================================
-- USERS TABLE
-- ============================================
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    role user_role NOT NULL DEFAULT 'MEMBER',
    status user_status NOT NULL DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- TEAMS TABLE
-- ============================================
CREATE TABLE teams (
    team_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    leader_id INT REFERENCES users(user_id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- TEAM MEMBERS (Many-to-Many)
-- ============================================
CREATE TABLE team_members (
    team_id INT REFERENCES teams(team_id) ON DELETE CASCADE,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (team_id, user_id)
);

-- ============================================
-- TASKS TABLE
-- ============================================
CREATE TABLE tasks (
    task_id SERIAL PRIMARY KEY,
    team_id INT REFERENCES teams(team_id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    created_by INT REFERENCES users(user_id) ON DELETE SET NULL,
    assigned_to INT REFERENCES users(user_id) ON DELETE SET NULL,
    status task_status NOT NULL DEFAULT 'TODO',
    priority task_priority NOT NULL DEFAULT 'MEDIUM',
    due_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- COMMENTS TABLE
-- ============================================
CREATE TABLE comments (
    comment_id SERIAL PRIMARY KEY,
    task_id INT REFERENCES tasks(task_id) ON DELETE CASCADE,
    author_id INT REFERENCES users(user_id) ON DELETE SET NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- ATTACHMENTS TABLE (Optional / BONUS)
-- ============================================
CREATE TABLE attachments (
    attachment_id SERIAL PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    uploaded_by INT REFERENCES users(user_id) ON DELETE SET NULL,
    task_id INT REFERENCES tasks(task_id) ON DELETE CASCADE,
    comment_id INT REFERENCES comments(comment_id) ON DELETE CASCADE,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- INDEXES
-- ============================================
CREATE INDEX idx_tasks_team_id ON tasks(team_id);
CREATE INDEX idx_tasks_assigned_to ON tasks(assigned_to);
CREATE INDEX idx_comments_task_id ON comments(task_id);
CREATE INDEX idx_team_members_user_id ON team_members(user_id);

-- ============================================
-- SAMPLE DATA
-- ============================================

-- Insert users (Admin, Team Leader, Member)
INSERT INTO users (username, email, password, name, surname, role, status)
VALUES
('admin', 'admin@gmail.com', '123', 'System', 'Admin', 'ADMIN', 'ACTIVE'),
('leader1', 'leader@gmail.com', '123', 'Alice', 'Smith', 'TEAM_LEADER', 'ACTIVE'),
('member1', 'member@gmail.com', '123', 'Bob', 'Brown', 'MEMBER', 'ACTIVE');

-- Create a sample team led by the team leader
INSERT INTO teams (name, description, leader_id)
VALUES
('Development Team', 'Handles all software development tasks', 2);

-- Add team members
INSERT INTO team_members (team_id, user_id)
VALUES
(1, 2),
(1, 3);

-- Create a sample task
INSERT INTO tasks (team_id, title, description, created_by, assigned_to, status, priority, due_date)
VALUES
(1, 'Implement Authentication', 'Develop user login and JWT auth system', 2, 3, 'TODO', 'HIGH', '2025-12-31');

-- Add a sample comment
INSERT INTO comments (task_id, author_id, content)
VALUES
(1, 3, 'Started working on JWT authentication module.');

-- ============================================
-- END OF SCRIPT
-- ============================================
