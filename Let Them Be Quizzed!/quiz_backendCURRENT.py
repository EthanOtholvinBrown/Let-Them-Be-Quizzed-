# -*- coding: utf-8 -*-
"""
Created on Mon May 11 20:43:40 2020

@author: cars_
"""
#Using Object Pool to store all objects
import os
from abc import ABC,abstractmethod
import requests
import json
#using factory and chain of responsibility pattern for quiz building
class Quiz_Factory():
    def create(quizType):
        if (quizType == "m"):
            mathQuiz = Math.build()
            return mathQuiz
        elif (quizType == "s"):
            spellingQuiz = Spelling.build()
            return spellingQuiz
        elif (quizType == "x"):
            mixQuiz = Mix.build()
            return mixQuiz
        elif (quizType == "t"):
            triviaQuiz = Trivia.build()
            return triviaQuiz

class Quiz(ABC):
    @abstractmethod
    def build(self):
        pass
class Math(Quiz):
    def build():         
        math_quiz = {}
        num_questions = int(input("How many questions are there?: "))
        os.system("cls")
        print("Enter the numbers and math type you want to quiz with: ")
        for count in range(num_questions):
            print("Question ",count+1)
            math_question = Math.mathQuestion()            
            math_quiz[count] = math_question
        return math_quiz
    def mathQuestion():
        math_elements = []
        num1 = int(input("Value 1: "))
        m_type = str(input("Type[+,-,*,/]: "))
        num2 = int(input("Value 2: "))
        if (m_type == "+"):
            answer = num1 + num2
        elif(m_type == "-"):
            answer = num1 - num2
        elif (m_type == "*"):
            answer = num1 * num2
        else:
            answer = num1 / num2
        math_elements= ["math",m_type, num1,num2, answer]
        return math_elements
    
    
        
class Spelling(Quiz):
    def build():
        num_questions = int(input("How many questions are there?: "))
        spelling_quiz = {}
        for count in range (num_questions):
            print("Question ",count+1)
            spelling_question = Spelling.spellingQuestion()
            spelling_quiz[count] = spelling_question
        return spelling_quiz
    def spellingQuestion():
        word= []
        os.system("cls")
        print("Enter the question [Must have a 1 word answer]: ")
        question = str(input()) 
        print("Enter the answer: ")
        word = str(input())
        word = ["spelling",word, question]
        return word
    
    
        
class Trivia (Quiz):
    def build():
        num_questions = int(input("How many questions are there?: "))
        trivia_quiz = {}
        for count in range (num_questions):
            print("Question ", count+1)
            trivia_question = Trivia.triviaQuestion()
            trivia_quiz[count] = trivia_question
        return trivia_quiz
    def triviaQuestion():
        trivia = []
        quests = requests.get("https://opentdb.com/api.php?amount=1")
        trivia_question = quests.json()
        ttype = trivia_question['results'][0]['type']
        tquestion = trivia_question['results'][0]['question']
        correct_answer = trivia_question ['results'][0]['correct_answer']
        incorrect_answers = trivia_question['results'][0]['incorrect_answers']
        trivia =["trivia",ttype,tquestion,correct_answer,incorrect_answers]
        return trivia
    
class Mix(Quiz):
    def build():
        mix_quiz = {}
        num = int(input("How many questions do you want to ask?: "))
        for count in range(num):
            os.system("cls")
            print("Enter question type for question ",count+1)
            print("m - Math")
            print("s - Spelling")
            print("t - Trivia")
            user_type = str(input())
            if(user_type == "m"):               
                math = Math.mathQuestion()
                mix_quiz[count] = math
            elif(user_type == "s"):
                spelling = Spelling.spellingQuestion()                
                mix_quiz[count] = spelling
            elif (user_type == "t"):
                trivia = Trivia.triviaQuestion()
                mix_quiz[count] = trivia
        return mix_quiz

            
class Check_Answers():
    def __init__(self,q_o):
        self.quiz = q_o
        
    def check_correct(self):
        self.correct = 0
        self.incorrect = 0
        for count in range (len(self.quiz)):
            os.system("cls")            
            if (self.quiz[count][0] == "math"):
                print("Question ",count+1)
                print("\n",self.quiz[count][2],self.quiz[count][1],self.quiz[count][3])
                self.user_answer = int(input("= "))
                if(self.quiz[count][4] == self.user_answer):
                    self.correct += 1
                else:
                    self.incorrect += 1
            elif (self.quiz[count][0] == "spelling"):
                print("Question ",count+1)
                print("\n",self.quiz[count][2])
                self.user_answer = str(input("Answer: "))
                if (self.quiz[count][1] == self.user_answer):
                    self.correct += 1
                else:
                    self.incorrect += 1
            elif (self.quiz[count][0] == "trivia"):
                if (self.quiz[count][1] == "multiple"):
                    print("Question ",count+1)
                    print("\n",self.quiz[count][2])
                    print("Enter one of: ")
                    print(self.quiz[count][3])
                    for num in range (len(self.quiz[count][4])):
                        print(self.quiz[count][4][num])
                    print(" ")
                    self.user_answer = str(input("Answer: "))
                    if (self.quiz[count][2] == self.user_answer):
                        self.correct += 1
                    else:
                        self.incorrect += 1
                elif (self.quiz[count][1] == "boolean"):
                    print("Question ",count+1)
                    print("\n", self.quiz[count][2])
                    self.user_answer = str(input("True or False? [case sensitive]: "))
                    if (self.quiz[count][2] == self.user_answer):
                        self.correct += 1
                    else:
                        self.incorrect += 1
                    
                    
    def get_grade(self):
        self.grade = (self.correct / len(self.quiz))*100
        return self.grade
