# explore_git_internals

## Exploring Git internals using Python
## Let's write `git log` in Python

Git is a powerful tool for source control. It's often misunderstood and abused.
Under the surface Git is an elegant and simple data structure. When you don't
understand that data structure, you don't really understand Git. It is flexible
enough to give you all the rope that you need to hang yourself in Git hell.
However, if you understand it, you’ll be in Git heaven.

Python is an elegant programming language heavily influenced by ABC "a teaching
language, a replacement for BASIC...." [1] It's a perfect tool that looks like
pseudo-code but executes. However, even with its simplicity, it is one of the
most powerful programming languages that exists. It is a perfect language to
document and run the Git data structure as we explore it.

In this talk, we start with a simple explanation of the Git data structure on
disk. We then explore coding to read those data structures and reconstruct a
`git log` command for any arbitrary git repository without using the `git`
command [2]. When finished, we should have our own working command that does
the same thing as `git log` for any arbitrary repository, on any branch. We'll
simply start at `HEAD` and work our way down the data structure.

Although it is not *useful* to have a Python version of Git, it is *fun*. Also,
this exploration helps you understand the Git tool on a much deeper level. When
you can program something, you can understand it. And, understanding Git helps
you be a better developer and collaborator.

## About the Speaker

Glen Jarvis has been programming Python for over 8 years and has been
programming in different languages for twenty plus years. He has been certified
in Linux/Unix administration by UC-Berkeley. Before that, he gained the highest
certification available for Informix database administration and supported
administrators. He is also certified in MongoDB as developer and administrator.
He is currently working on his AWS certification.

He has worked for companies such as IBM, UC-Berkeley, Sprint and Silicon Valley
Start-ups. He has worked in the fields of Databases, Data Science,
Bioinformatics and Web Technologies. He has been exclusively working in DevOps
the past year.

Glen has been working for almost three years at RepairPal, a successful
start-up that gives you free estimates for what your car repair *should*
cost [3]. He is currently putting the "Dev" in "DevOps" using Ansible (and
Ruby). He additionally owns a consulting and training company, Glen Jarvis,
LLC, that mentors budding programmers. Some of his training Videos include How
to create a free AWS instance [4], Ansible Hands-On Training [5], and An
introduction to Test Driven Development [6].  He has also been an open source
contributor [7] and a member and co-organizer of the Bay Area Python Interest
Group (BayPIGgies) [8].

## Sponsored by BayPIGgies and Silicon Valley Python MeeetUp

This is a collaboration between Silicon Valley Python MeeetUp [9] and the Bay Area Python Interest Group (BayPIGgies) [8].  Join their mailing list [10].


[1] http://python-history.blogspot.com/2009/02/early-language-design-and-development.html

[2] With one small caveat. There is only one plumbing command used to read a binary file `git cat-file`. All other files are just text and can be read easily.

[3] http://repairpal.com/

[4] https://www.youtube.com/watch?v=tmNgXQXkpWs

[5] https://www.youtube.com/watch?v=w8fOEEMqpOw

[6] https://www.youtube.com/watch?v=sNgmSiesOG0

[7] https://github.com/glenjarvis/

[8] http://baypiggies.net/

[9] http://www.meetup.com/silicon-valley-python/

[10] https://mail.python.org/mailman/listinfo/baypiggies


## Slides

https://docs.google.com/presentation/d/1d1x2FsYEGsmZ662USFCloG4Aad1rXaXdvFHWgFu-clY/edit?usp=sharing

## Videos

There are currently no video recordings for this talk. When recordings are made, references will be made here.
