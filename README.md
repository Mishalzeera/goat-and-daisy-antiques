## Introduction and basic features

An online antique store that also provides restoral and repair services, 
built using Django. The store uses custom CMS for seperate sales and repair
departments. A user who wishes to buy does not need to create an account, but
can if she so wishes. A user who wishes to have repairs or restorals done, on
the other hand, must create an account in order to keep track of their specific
requests, materials etc. 


## Test Driven Development approach

The Django docs state (in the Poll app introduction walkthrough, testing
section) that many developers will not take any code seriously, however well 
created, without robust testing built in. This makes sense after my previous
experience with Flask - towards the end, so much time was spent manually 
creating accounts and testing different things that could have been put to 
better use. It was indeed difficult to understand why some things were 
happening, and it would have been very useful to have had a set of tests to
run. 

For this project, I will perhaps create something less complex than some 
projects, but will rather ensure that there is sufficient testing. The goal 
is to ensure that every view, model, form, function etc will have a 
corresponding test class in the appropriate location. My goal is that by the 
time the app matures, the tests save me enough time to put a little more 
energy and attention into the CSS and Javascript, for example. 

The Test Driven Development approach is recommended by many senior software
engineers, and it will be a good experience to try and take that approach on
board. Furthermore, I can imagine that when interacting with a preexisting 
codebase and its complex testing mechanics, having some confidence with the 
way testing works will help. I can imagine the amount of stress it would be
to interact with a large, sensitive body of code and not be sure if my
additions are having unintended consequences. 
