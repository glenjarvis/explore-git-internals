## Exploring Git internals using Python
## Let's write `git log` in Python

Git is a powerful tool for source control. It's often misunderstood and abused.
Under the surface Git is an elegant and simple data structure. When you don't
understand that data structure, you don't really understand Git. It is flexible
enough to give you all the rope that you need to hang yourself in Git hell.
However, if you understand it, you are released from Git hell.

Python is an elegant programming language heavily influenced by ABC "a teaching
language, a replacement for BASIC...." [1] It's a perfect tool that looks like
pseudo-code but executes. However, even with its simplicity, it is one of the
most powerful programming languages that exists. It is a perfect language to
document and run the Git data structure as we explore it.

In this talk, we start with a simple explanation of the Git data structure on
disk. We use Python to read those data structures and reconstruct a `git log`
command for any arbitrary git repository. When finished, we should have our
own working command that does the same thing as `git log` for any arbitrary
repository, on any branch. We'll simply start at `HEAD` and work our way down
the data structure.

Although it is not *useful* to have a Python version of Git, it is *fun*. Also,
this exploration helps you understand the Git tool on a much deeper level. When
you can program something, you can understand it. And, understanding Git helps
you be a better developer and collaborator.

[1] http://python-history.blogspot.com/2009/02/early-language-design-and-development.html

## About the Speaker

Glen Jarvis has been programming Python for over 8 years and has been
programming in different languages for over twenty years. He has been certified
in Linux/Unix administration by UC-Berkeley. Before that, he gained the highest
certification available for Informix database administration and supported
administrators. He is also certified in MongoDB as developer and administrator.
He is currently working on his AWS certification.

He has worked for companies such as IBM, UC-Berkeley, Sprint and many Silicon
Valley Start-ups. He has worked in the fields of Databases, Data Science,
Bioinformatics and Web Technologies. He has been exclusively working in DevOps
the past year.

Glen has been working for almost three years at RepairPal, a successful start-up
that gives you free estimates for what your car repair *should* cost [1]. He is
currently putting the "Dev" in "DevOps" using Ansible (and Ruby). He additionally
owns a consulting and training company, Glen Jarvis, LLC, that mentors budding
programmers. Some of his training Videos include How to create a free AWS
instance, Ansible Hands-On Training, and An introduction to Test Driven
Development. He has also been an open source contributor and a member and
co-organizer of the Bay Area Python Interest Group (BayPIGgies) [2].

[1] http://repairpal.com/

[2] http://baypiggies.net/



## PyBay

This talk given on 20-Aug at PyBay: http://www.pybay.com/


## BayPIGgies / Silicon Valley Python MeeetUp

This talk given on 24-June as a collaboration between Silicon Valley Python MeeetUp [9] and the Bay Area Python Interest Group (BayPIGgies) [1][2].

[1] http://www.meetup.com/silicon-valley-python/

[2] http://baypiggies.net/


## Slides

https://docs.google.com/presentation/d/1d1x2FsYEGsmZ662USFCloG4Aad1rXaXdvFHWgFu-clY


## Videos

June, 2016: Bay Area Python Interest Group (BayPIGgies): http://baypiggies.net
  https://www.youtube.com/watch?v=CB9p8n3gugM

## Disclaimer

The code in this repository was meant to be a toy example. I should have
embraced that and ignored handing gpg signatures when parsing the commit (we do
successfully handle that case but it added complexity).

We did not, however, handle the complexity of properly handling all history for
merges. We naively just picked one parent (even if there were two like one
would see in a merge). This means we skip one branch of history. In other
words, imagine this scenario into a new directory:

```
mkdir git_demo
cd git_demo
git init
touch 1
git add 1
git commit -m "Add 1"
git branch branch1
touch 2
git add 2
git commit -m "Add 2"
git checkout branch1
touch 3
git add 3
git commit -m "Add 3"
git checkout master
git merge branch1
git log
```

Then the "Add 2" commit wouldn't be shown in the history even though all files
would be present. This is currently intentional. I only wish I was disciplined
enough to also ignore the GPG case (which I did handle).
