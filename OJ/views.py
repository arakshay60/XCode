from django.shortcuts import render,get_object_or_404
from .models import Problem,TestCase
from Users.models import Submission,User
from OJ.forms import Code
from django.contrib.auth.decorators import login_required
import subprocess
from django.utils import timezone
from django.conf import settings
import os
from datetime import datetime
from time import time
# Create your views here.
def homePage(request):
    return render(request,'OJ/main.html')

def problemPage(request):
    user=request.user if request.user.is_authenticated else None
    problems=Problem.objects.all()

    
    problem_list=[]
    for problem in problems:
        submission=Submission.objects.filter(user=user,problem=problem,verdict='Accepted')
        if submission:
            solved=True
        else:
            solved=False
        problem_list.append(
            {
                'id':problem.id,
                'title':problem.title,
                'difficulty':problem.get_difficulty_display(),
                'status':'Solved' if solved else 'Unsolved'
            }
        )
    return render(request,'OJ/problems.html',{'problem_list':problem_list})

def descriptionPage(request,problem_id):
    user=request.user if request.user.is_authenticated else None
    problem=get_object_or_404(Problem,id=problem_id)
    form=Code()
    context={'user':user,'problem':problem,'code_form':form}
    return render(request,'OJ/description.html',context)

@login_required(login_url='login')
def leaderBoard(request):
    users=User.objects.all()
    context={'users':users}
    return render(request,'OJ/leaderboard.html',context)

@login_required(login_url='login')
def verdictPage(request,problem_id):
    if request.method=='POST': 

        form=Code(request.POST)
        testcases=TestCase.objects.filter(problem_id=problem_id)
        problem=get_object_or_404(Problem,id=problem_id)
        code=''
        language=''
        score=0
        if problem.difficulty=='E':
            score=3
        elif problem.difficulty=='M':
            score=5
        else:
            score=10
        
        if form.is_valid():
           
            code=form.cleaned_data.get('code')
            code = code.replace('\r\n','\n').strip()
            language=form.cleaned_data.get('language')
  
     
        verdict='Wrong Answer'    
        submission=Submission(user=request.user,problem_id=problem_id,code=code,verdict=verdict,sub_time=timezone.now()
                               ,language=language)
        submission.save()
        extension=''
        compile=''
        run=''
        compile_file=''
        filename=str(submission.id)

        if language=='C++':
            extension='.cpp'
            compile=f'g++ -o {filename}.exe {filename}.cpp'
            run=f'{filename}.exe'
            compile_file=f'{filename}.exe'
 

        elif language=='Python3':
            extension='.py'
            compile='python'
            run=f'python {filename}.py'
            compile_file=f'{filename}.py'
        else:
            filename='Main'
            extension='.java'
            compile=f'javac {filename}.java'
            run=f'java {filename}'
            compile_file=f'{filename}.class'

        file=filename+extension
        filepath=f'{settings.FILES_DIR}/{file}'
        codefile=open(filepath,'w')
        codefile.write(code)
        codefile.close()



        if language!='Python3':
            cmp=subprocess.run(f"{compile}",shell=True,capture_output=True,cwd=settings.FILES_DIR) 
        
        comments=""
        flag=False
        if language!='Python3' and cmp.returncode!=0  :
            verdict='Compilation Error'
            submission.stderr=cmp.stderr.decode('utf-8')
        else:
            for index,testcase in enumerate(testcases):
                tfile=f'{index}.txt'
                tfilepath=f'{settings.FILES_DIR}/{tfile}'
                test=open(tfilepath,'w')
                test.write(testcase.input.replace('\r\n', '\n').strip())
                test.close()
                
                start=time()
                result = subprocess.run(f'{run} < {tfile}', capture_output=True,text=True, timeout=problem.time_limit, shell=True, cwd=settings.FILES_DIR)
                
        
                if result.returncode!=0:
                    flag=True
                    verdict='Runtime Error'
                    submission.stderr=result.stderr
                    os.remove(tfilepath)
                    break
                else:
                    result.stdout=result.stdout.replace('\r\n', '\n').strip()
                    testcase.output=testcase.output.replace('\r\n', '\n').strip()
                    if result.stdout!=testcase.output:
                        flag=True
                        comments=f'Testcase{index+1} failed:\n {testcase.input} \n Expected Output: \n {testcase.output} \n Your Output:{result.stdout}'
                        submission.stdout=result.stdout
                        os.remove(tfilepath)
                        break
                os.remove(tfilepath)

            
            if flag==False:
                    verdict='Accepted'
            if verdict=='Wrong Answer':
                    testcase.output+='\n'
                    if result.stdout==testcase.output:
                        verdict='Accepted'
        #print(result.stdout)
        #print(testcase.output)
        

        if language!='Python3' and cmp.returncode==0 :
                os.remove(f'{settings.FILES_DIR}/{compile_file}')
            

        prev_sub=Submission.objects.filter(user=request.user,problem_id=problem_id,verdict='Accepted')
        if len(prev_sub)==0 and verdict=='Accepted' :
            request.user.total_score+=score

        request.user.save()
        submission.verdict=verdict
        submission.save()
    
        os.remove(filepath)
        context={'verdict':verdict,'comments':comments,'submission':submission}
        return render(request,'OJ/verdict.html',context)
    

@login_required(login_url='login')
def submissionPage(request):
    submissions=Submission.objects.filter(user=request.user)
    context={'submissions':submissions}
    return render(request,'OJ/submission.html',context)

@login_required(login_url='login')
def submissionCode(request,submission_id):
    submission=Submission.objects.get(id=submission_id)
    context={'submission':submission}
    return render(request,'OJ/submission_code.html',context)