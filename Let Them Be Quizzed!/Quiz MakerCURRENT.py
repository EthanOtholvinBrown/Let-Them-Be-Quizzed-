# -*- coding: utf-8 -*-
"""
Created on Mon May 11 23:00:26 2020
This program was created with the intention of providing an easy to use
method for creating and administering quizzes to students. It was meant
for parents who need to teach from home or teachers who need to teach
virtually. The program is able to create and administer quizzes while
keeping track of students, grades and teachers. 

*DISCLAIMER*

Currently the program is not fully functional due to the cloud database
being disconnected. It was temporarily utilized for proof of concept but
is no longer in service. To use this program a replacement service is needed.


@author: Ethan Brown
"""
import quiz_backendCURRENT as quiz
import time
import os
import redis
import pickle
#CURRENT REDIS CALL IS INVALID
#IT WAS TEMPORARY FOR THE DURATION OF THE PROJECT
#REQUIRES NEW DATABASE FOR FULL FUNCTIONALITY
r = redis.Redis(
    host = 'LINK TO HOST HERE',
    port = 'INSERT PORT HERE',
    password = 'INSERT PASSWORD HERE',
    decode_responses=False
    )
quizzes = []
students = {}
grades_dict = {}
quiz_storage = {}

def main():  
    print("Welcome To 'Let Them Be Quizzed'!")
    print("This program is going to help you build and administer quizes.")
    print("Let's begin!")
    print("Press any key to continue...")
    userChoice = str(input())
    time.sleep(3)
    userChoice = "null"    
    os.system('cls')
    teacherName = str(input("Enter your name[Case Sensitive]: "))
    while(userChoice != "q"):        
        os.system('cls')
        #Main menu
        print("Welcome ",teacherName,"!")
        print("Main Menu: ")
        print("'b' - Build a quiz")
        print("'d' - Display available quizzes")
        print("'a' - Administer a quiz")
        print("'l' - List the available students")
        print("'g' - Display a specific student's grades")
        print("'r' - Recall a teacher's data")        
        print("'s' - Save current report")
        print("'q' - Quit")
        userChoice = str(input("Entry: "))
        #using MVC Model for quiz use
        if (userChoice == "b"):
            os.system("cls")            
            quizName = str(input("What do you want to call this quiz?: "))
            quizzes.append(quizName)
            os.system("cls")
            os.system("cls")
            print("What type of quiz is it?")
            print("m - Math")
            print("s - Spelling")
            print("t - Trivia")
            print("x - Mix")
            qType = str(input("Entry: "))
            os.system("cls")   
            #Math type question
            if(qType == "m"):        
                math = quiz.Quiz_Factory.create(qType)
                quiz_storage[quizName] = math 
            #Spelling question                              
            elif (qType == "s"):
                spelling = quiz.Quiz_Factory.create(qType)
                quiz_storage[quizName] = spelling
            #Mix
            elif(qType == "x"):
                mix = quiz.Quiz_Factory.create(qType)
                quiz_storage[quizName] = mix
            #Trivia based on API
            elif (qType == "t"):
                trivia = quiz.Quiz_Factory.create(qType)
                quiz_storage[quizName] = trivia
            else:
                print("That is not a valid option.")
                print("Returning to top...")
                time.sleep(3)
            quiz_pickle = pickle.dumps(quiz_storage)
            r.hset(teacherName,"Quizzes",quiz_pickle)
        elif (userChoice == "d"):
            os.system("cls")
            if not quizzes:
                print("There are no quizzes!")
                print("Returning to main...")
                time.sleep(3)
            else:
                print("Quizzes you've built:")                
                get_quizzes(quizzes)
                print("Press any key to return to main or 'q' to quit program...")
                userChoice = str(input())
        elif (userChoice == "a"): 
            os.system("cls")
            if not quiz_storage:
                print("There are no quizzes!")
                print("Returning to main...")
                time.sleep(3)
            else:                 
                students = studentQuiz(quizzes,quiz_storage,teacherName)                
                                
        elif (userChoice == "g"):
            try:
                checkGrade(students)
            except UnboundLocalError:
                print("There are no students!")
                print("Returning to main...")
                time.sleep(3)
        elif (userChoice == "l"):
            os.system("cls")
            try:
                if not students:
                    print("There are no stored students!")
                    print("Returning to main menu...")
                    time.sleep(3)
                else:
                    print("Stored students for ",teacherName,": ")
                    get_students(students)
                    print("Press any key to return to main or 'q' to quit program...")
                    userChoice = str(input())
            except UnboundLocalError:
                print("There are no students!")
                print("Returning to main menu...")
                time.sleep(3)
        
        elif(userChoice == "r"):
            os.system("cls")
            oldName = str(input("Enter the teacher's name[Case sensitive]: "))
            checkifExists = r.exists(oldName)
            os.system("cls")
            if (checkifExists == 1):
                try:
                    old_quizzes = pickle.loads(r.hget(oldName,"Quizzes"))
                except TypeError:
                    print("There are no quizzes stored")
                try:
                    old_students = pickle.loads(r.hget(oldName,"Students"))
                except TypeError:
                    print("There are no students stored")
                
                recallChoice = "null"
                while (recallChoice != "b"):
                    old_quiz_name = [] 
                    os.system("cls")
                    print("Recall Menu for ",oldName,": ")
                    print("'qu' - Display the list of available quizzes(Ignore if there are none)")
                    print("'st' - Display the stored students(Ignore if there are none)")
                    print("'a' - Administer quiz")
                    print("'d' - Display grade")
                    print("'b' - Back to main menu")
                    print("Or press any other key to go back")
                    recallChoice = str(input("Entry: "))
                    if (recallChoice == "qu"):
                        os.system("cls")
                        print("Stored Quizzes: ")
                        for qn in old_quizzes:    
                            print(qn)                            
                        print("Press any key to return to recall menu...")
                        recallChoice = str(input())
                    elif (recallChoice == "st"):
                        os.system("cls")
                        print("Stored Students: ")
                        get_students(old_students)
                        print("Press any key to return to recall menu...")
                        recallChoice = str(input())
                    elif(recallChoice == "a"):
                        for qn in old_quizzes:
                            old_quiz_name.append(qn)
                        students = studentQuiz(old_quiz_name,old_quizzes,teacherName)
                    elif (recallChoice == "d"):
                        checkGrade(old_students)
                    elif (recallChoice == "b"):
                        os.system("cls")
                        print("Returning to main menu...")
                        time.sleep(3)
            elif (checkifExists == 0):
                os.system("cls")
                print("That teacher does not exist!")
                print("Returning to main menu...")
                time.sleep(3)
                
            
        elif (userChoice == "s"):
            os.system("cls")
            print("What do you want to save the report as?[make sure to end in filetype]")
            rname = str(input())
            createReport(students,rname,teacherName)
        elif(userChoice == "q"):
            os.system("cls")
            print("Goodbye!")
            time.sleep(3)
            break
        else:  
            os.system("cls")
            print("Not a valid option.")
            print("Returning to main...")
            time.sleep(3)
def get_students(students):
    for stu ,d in students.items():
        print(stu)
def get_quizzes(quizzes):
    print("Available Quizzes:")
    for count in range(len(quizzes)):        
        print(quizzes[count])
def studentQuiz(quizzes,quiz_storage,teacherName):
    exists = 0
    os.system("cls")
    studentName = str(input("Enter the name of the student: "))
    os.system("cls")
    print("Enter a quiz for ",studentName," to take")
    get_quizzes(quizzes) 
    userChoice = str(input("Your choice: "))
    for check in range (len(quizzes)):
        while (exists == 0):
            if (userChoice == quizzes[check]):
                exists = 1
            else:
                exists = 0  
                os.system("cls")
                print("Inavlid - Enter an available quiz")
                get_quizzes(quizzes)
                userChoice = str(input("Your Choice: "))
    time.sleep(3)
    os.system("cls")    
    giveQuiz = quiz.Check_Answers(quiz_storage[userChoice])
    giveQuiz.check_correct()
    quizGrade = giveQuiz.get_grade()                
    grades_dict[userChoice] = quizGrade
    students[studentName] = grades_dict
    student_pickle = pickle.dumps(students)
    r.hset(teacherName,"Students",student_pickle)
    return students    
    print("Invalid - Enter a quiz name...")
    studentQuiz(quizzes,quiz_storage,teacherName)
def checkGrade(students):
    os.system("cls")
    if not students:
        print("There are no stored students!")
        print("Returning to main menu...")
        time.sleep(3)
    else:
        print("Stored students: ")
        for stu ,d in students.items():
            print(stu)
        print("Which student's grades do you want to see?")
        name = str(input())
        os.system("cls")
        for s, n in students.items():
            if (s == name):                    
                print(s)
                for s2,n2 in n.items():
                    print("\nQuiz: ",s2)
                    print("Grade: ", n2)
        print("Press any key to return to main program...")
        userChoice = str(input())
def createReport(students,reportName,teacherName):
    resultFile = open(reportName,"w") 
    resultFile.write("Report for ")
    resultFile.write(teacherName)
    for sn, q in students.items():
        resultFile.write("\nStudent Name: ")
        resultFile.write(sn)
        for qn,g in q.items():
            resultFile.write("\nQuiz: ")
            resultFile.write(qn)
            resultFile.write("\nGrade: ")
            resultFile.write(str(g))                        
    resultFile.close()
main()        