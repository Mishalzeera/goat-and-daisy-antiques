## Introduction and basic features

An online antique store that provides restoral and repair services, 
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

For this project, I will ensure that there is sufficient testing. The goal 
is to that every view, model, form, function etc will have a 
corresponding test in the appropriate location. My goal is that by the 
time the app matures, the tests save me enough time to put a little more 
energy and attention into the CSS and Javascript, for example. 


## The User(s)

### The Customer

The average G&D customer is someone who is relatively tech savvy, in the sense
of having social media accounts. They are confident enough with apps that have 
food delivered to the house and apps like Uber and Spotify. This gives them
the confidence to interact with the hybrid online/real-life service that
G&D offers them. They have good taste and an eye for good design. 

### The Staff Member

The small staff at G&D are split into two camps, broadly speaking. Those to do 
with the shop and those to do with the repairs and restorals. They have limited
permissions to interact with the site functionality depending on their roles.


## The Shop

A small online store that sells antique furniture and curiousities. The small
size of the inventory reinforces a boutique feel. Customers can buy things 
without creating an account. Creating an account allows the customer to save 
delivery information etc. 


## The Workshop

The workshop is designed for close collaboration with the staff and customers.
There is also a mutual accountability between staff and customers. Customers
are obligated to create an account, which allows the staff to refer to 
style guides that the customer supplies. Staff creates records of changes that
customers sign off on. Materials to be ordered, a running account of extra 
costs and a dynamic total cost that is updated whenever anything changes. The
idea is not to replace an in-person experience, but to provide the customer 
with a creative opportunity to collaborate more deeply and have more peace of
mind. 



