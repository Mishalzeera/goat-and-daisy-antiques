| Test Label |Test Action  |Expected Outcome|Test Outcome|
|--|--|--|--|
|Navigate to site|Enter the base URL |Auto-redirects to **Index**|PASS |
|Special Admin nav dropdown|Log in with Admin perms|Upon login, gain access to unique links - Staff Management, Admin Panel|PASS|
|Staff Management|Follow link|Gives Admin the ability to create an employee in the system with a linked Auth account, provisional password which the employee can change later, group permissions set|PASS|
|View All Staff|Follow link in Staff Management|Gives easy overview CRUD of all employees with two notes field - one shared with the employee and one private|PASS|
|Admin Panel|Follow link|This leads to the all powerful Admin Panel created by Django, which in this case is restricted to Admin only|PASS|