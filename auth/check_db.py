"""Quick script to check the database contents"""
import sqlite3

conn = sqlite3.connect('auth_system.db')
cursor = conn.cursor()

# Get all users
cursor.execute('SELECT id, email, is_active, role, created_at FROM users')
users = cursor.fetchall()

print('\n' + '='*80)
print('SQLITE DATABASE CONTENTS')
print('='*80)
print(f'Database file: auth_system.db')
print(f'Total users: {len(users)}')
print('='*80)

if users:
    for user in users:
        print(f'\nUser ID: {user[0]}')
        print(f'  Email: {user[1]}')
        print(f'  Active: {user[2]}')
        print(f'  Role: {user[3]}')
        print(f'  Created: {user[4]}')
        print('-'*80)
else:
    print('No users found in database.')

conn.close()
