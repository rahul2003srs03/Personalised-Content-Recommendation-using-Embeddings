# -*- coding: utf-8 -*-
"""
Question content for the Capgemini Exceller practice PDF.

Markup reference (parsed by build_pdf.parse):
    #PART t   #SET t   #SEC t   #SUB t
    #Q n|text        #C ... #E        #O options
    #P text   #B text  #N note   #K key line   #SP n   #PB
"""

FRONT = r"""
#PART How To Use This Book
#P This book holds ten complete practice sets modelled on the Capgemini Exceller online assessment. Sets 1 to 5 sit at the standard Analyst band. Sets H1 to H5 are deliberately harder and target the Senior Analyst band, the track that carries the higher package.
#P Each set is structured the same way as the live assessment.

#SUB Structure of every set
#C
Section A   Pseudo-code (20 Q) + Computer Fundamentals (10 Q)     30 min
Section B   English Communication                                 10 min
Section C   Game-Based Cognitive (Aon smartPredict formats)        8-10 min
Section D   Coding Round (2 problems)                             45 min
#E

#SUB Rules that mirror the live test
#P There is no negative marking anywhere in the assessment, so leave nothing blank. Every section is an elimination gate with its own cut-off, and you only reach the next section by clearing the current one. The live test is AI proctored on the Superset platform.
#P Section A cut-off: aim for 70 percent on Sets 1 to 5. On Sets H1 to H5, 55 to 65 percent is a strong result and is not a failing signal against real cut-offs.
#P Section B cut-off: aim for 65 percent.
#P Section C is scored on accuracy and response latency together, so time yourself per item, not only per section.
#P Section D determines the band. One problem fully passing maps to the middle band, both problems to the top band.

#SUB Reported band mapping
#C
Both coding problems solved completely      7.50 LPA   (A5)
One coding problem solved completely        5.75 LPA   (A4)
All rounds cleared, partial coding          4.00 - 4.50 LPA   (A3)
#E
#N Capgemini does not publish official cut-offs or band criteria. The figures above are aggregated candidate reports and should be treated as directional.

#SUB Languages for the coding round
#P C, C++ and Java. Reported guidance is that Python is not permitted in the Exceller coding round, though sources conflict on this point. Prepare in C, C++ or Java.

#PB
#PART Notation Reference

#SUB Pseudo-code notation
#P Capgemini writes pseudo-code in a fixed notation. It is not a real language and no syntax knowledge is required. What is tested is your ability to trace variable state through the instructions.
#C
Integer a, b, c            declaration
Integer Array[5]           array declaration
Set a = 5, b = 3           assignment
for(each i from 1 to n)    counting loop, inclusive of both bounds
for(each i from n down to 1)   descending loop
End for                    loop terminator
while(condition)            End while
repeat ... until(condition)     post-tested loop
if(cond)  else if(cond)  else   End if
MOD        integer remainder
/          INTEGER division - the fractional part is discarded
AND OR XOR bitwise operators
>>  <<     right and left bit shift
LENGTH(s)  string length
s[i]       character at index i, zero based
Print      output
End function name()         function terminator
#E

#SUB Five pseudo-code patterns that dominate the bank
#P Accumulator loops - running sums and products over a bounded range. The trap is the exit condition; i less-than-or-equal-to n versus i less-than n changes the iteration count by one.
#P Modulo conditionals - nested if and else on divisibility or parity. The trap is losing track of which else pairs with which if.
#P String traversal - character iteration with LENGTH and indexing. The traps are treating LENGTH as the last valid index instead of length minus one, and confusing a character value with its position.
#P Number-theory routines - Euclidean GCD, digit sums, digit counts, base conversion. All built on repeated MOD and integer division, and they terminate in a handful of steps, so a full trace is always feasible.
#P Array swap and partial sort - you are given a starting array and asked for its state after exactly k iterations, not after the sort completes.

#SUB Game-based notation used in this book
#P The live games render coloured shapes and live animation. Printed pages cannot, so this book uses fixed ASCII tokens. The logic is identical.
#C
STR = star        CIR = circle       TRI = triangle
SQR = square      PLS = plus         DIA = diamond

In grid questions:     X = cell holds a dot        . = empty cell
Arithmetic operators:  *  multiply    /  divide    +  add    -  subtract
#E

#SUB switchChallenge - how the operator works
#P This is the deductive-logic game, and the one most worth drilling. Two rows of symbols are shown: an input row on top and an output row below. An operator is a string of digits. The digit in position k names which INPUT position supplies the symbol for OUTPUT position k.
#C
Input     A  B  C  D
Operator  3  1  4  2
Output    C  A  D  B

Read it as:  output slot 1 takes input 3
             output slot 2 takes input 1
             output slot 3 takes input 4
             output slot 4 takes input 2
#E
#P Levels escalate: one operator, then two operators with one of them hidden, then three with the middle hidden, then four. Six minutes, adaptive.
#P Two techniques carry the whole game. First-digit elimination: find the first output symbol in the input row, note its position, and discard every option that does not begin with that digit. Single-symbol tracking: follow one distinctive symbol forward from the input and backward from the output, and read off only the digit you need.
#P Learn to invert an operator directly. To invert 3142, ask where each input position lands: input 1 goes to slot 2, input 2 to slot 4, input 3 to slot 1, input 4 to slot 3, giving 2413. Several harder items in this book reduce to a single inversion.

#SUB gridChallenge
#P Alternating rounds. Memorise dot positions in a grid, then answer a spatial distractor - mirror symmetry, diagonal symmetry, or rotation - then recall the dots. The distractors exist specifically to overwrite your visual memory. Three to five memory rounds, adaptive, six minutes.
#P Convert positions to verbal labels such as row two far right rather than holding a picture. Verbal and visual memory use partly separate channels, so labelling survives the interference. Do not skip the spatial questions; failing them caps how far the adaptive algorithm will push you even with perfect recall.

#SUB digitChallenge
#P Complete an arithmetic equation by filling the blanks with digits 1 to 9, each digit used only once per equation. Standard operator precedence applies. Throughout this book at least one wrong option reaches the target value while reusing a digit, which is the real discriminator. Check distinctness before you check arithmetic.

#SUB motionChallenge
#P Live object tracking and complex control. Printed pages cannot animate, so this book uses a discrete-tick form: a ball moves one cell per tick on a grid and reflects off any wall it strikes. On a corner both components reverse at once. The underlying skill, holding a rule while updating state under time pressure, is the same.
"""

SET1 = r"""
#SET Test Set 1
#N Standard Analyst band. Section A 30 min, Section B 10 min, Section C 8 min, Section D 45 min.

#SEC Section A - Pseudo-code (Q1 to Q20)

#Q 1
#C
Integer a, b, c
Set a = 8, b = 3
c = a MOD b
a = c << 2
Print a + b + c
#E
#O A) 11     B) 13     C) 15     D) 8

#Q 2
#C
Integer p, q, r
Set p = 4, q = 2, r = 1
r = (p AND q) OR (r + 1)
Print r
#E
#O A) 0     B) 1     C) 2     D) 3

#Q 3
#C
Integer sum, i
Set sum = 0
for(each i from 1 to 6)
  if(i MOD 2 == 0)
    sum = sum + i
  else
    sum = sum - i
  End if
End for
Print sum
#E
#O A) 3     B) -3     C) 21     D) 9

#Q 4
#C
Integer solve(Integer n)
  Integer c
  Set c = 0
  while(n > 0)
    c = c + (n MOD 10)
    n = n / 10
  End while
  return c
End function solve()
Print solve(4728)
#E
#O A) 17     B) 21     C) 11     D) 4

#Q 5
#C
Integer a, b
Set a = 20, b = 6
while(a != b)
  if(a > b)
    a = a - b
  else
    b = b - a
  End if
End while
Print a
#E
#O A) 1     B) 2     C) 4     D) 6

#Q 6
#C
Integer Array[5]
Set Array = {3, 7, 2, 9, 4}
Integer i, m
Set m = Array[0]
for(each i from 1 to 4)
  if(Array[i] < m)
    m = Array[i]
  End if
End for
Print m
#E
#O A) 2     B) 3     C) 9     D) 4

#Q 7
#C
Integer x, y
Set x = 5, y = 2
x = x / y
y = x * y
Print x, y
#E
#O A) 2 4     B) 2.5 5     C) 2 5     D) 3 6

#Q 8
#C
String s
Set s = "PROGRAM"
Integer i, c
Set c = 0
for(each i from 0 to LENGTH(s) - 1)
  if(s[i] == 'R')
    c = c + 1
  End if
End for
Print c
#E
#O A) 1     B) 2     C) 3     D) 0

#Q 9
#C
Integer n, f
Set n = 4, f = 1
while(n > 1)
  f = f * n
  n = n - 1
End while
Print f
#E
#O A) 12     B) 24     C) 10     D) 6

#Q 10
#C
Integer a, b, c
Set a = 12, b = 5
c = a XOR b
Print c
#E
#O A) 7     B) 9     C) 13     D) 4

#Q 11
#C
Integer i, j, c
Set c = 0
for(each i from 1 to 3)
  for(each j from i to 3)
    c = c + 1
  End for
End for
Print c
#E
#O A) 6     B) 9     C) 3     D) 5

#Q 12
#C
Integer fun(Integer n)
  if(n <= 1)
    return n
  End if
  return fun(n - 1) + fun(n - 2)
End function fun()
Print fun(6)
#E
#O A) 5     B) 8     C) 13     D) 6

#Q 13
#C
Integer n, r, rev
Set n = 132, rev = 0
while(n > 0)
  r = n MOD 10
  rev = rev * 10 + r
  n = n / 10
End while
Print rev
#E
#O A) 231     B) 132     C) 213     D) 321

#Q 14
#C
Integer a, b, t
Set a = 3, b = 8
t = a
a = b
b = t
Print a - b
#E
#O A) -5     B) 5     C) 11     D) 0

#Q 15
#C
Integer Array[6]
Set Array = {1, 2, 3, 4, 5, 6}
Integer i, s
Set s = 0
for(each i from 0 to 5)
  if(i MOD 2 == 0)
    s = s + Array[i]
  End if
End for
Print s
#E
#O A) 9     B) 12     C) 21     D) 6

#Q 16
#C
Integer x, c
Set x = 1, c = 0
while(x < 100)
  x = x * 3
  c = c + 1
End while
Print c
#E
#O A) 4     B) 5     C) 6     D) 3

#Q 17
#C
Integer a, b, c
Set a = 10, b = 20, c = 30
a = a + b
b = a - b
c = a - b
Print a, b, c
#E
#O A) 30 10 20     B) 10 20 30     C) 30 20 10     D) 20 10 30

#Q 18
#C
Integer n, c, i
Set n = 29, c = 0
for(each i from 1 to n)
  if(n MOD i == 0)
    c = c + 1
  End if
End for
Print c
#E
#O A) 1     B) 2     C) 29     D) 0

#Q 19
#C
Integer p, q
Set p = 16, q = 0
while(p > 1)
  p = p >> 1
  q = q + 1
End while
Print q
#E
#O A) 3     B) 4     C) 5     D) 16

#Q 20
#C
Integer Array[5], i, t
Set Array = {5, 1, 4, 2, 8}
for(each i from 0 to 3)
  if(Array[i] > Array[i+1])
    t = Array[i]
    Array[i] = Array[i+1]
    Array[i+1] = t
  End if
End for
Print Array[4]
#E
#O A) 5     B) 8     C) 2     D) 1

#SEC Section A - Computer Fundamentals (Q21 to Q30)

#Q 21|Time complexity of binary search on a sorted array of n elements?
#O A) O(n)     B) O(log n)     C) O(n log n)     D) O(1)

#Q 22|Which OOP concept lets one function name work with different parameter lists?
#O A) Encapsulation     B) Inheritance     C) Polymorphism     D) Abstraction

#Q 23|In C, the size of a pointer on a 64-bit system is:
#O A) 2 bytes     B) 4 bytes     C) 8 bytes     D) Depends on the pointed-to type

#Q 24|Which SQL clause filters groups after aggregation?
#O A) WHERE     B) HAVING     C) GROUP BY     D) ORDER BY

#Q 25|A stack follows which order?
#O A) FIFO     B) LIFO     C) Priority     D) Random

#Q 26|Which normal form eliminates transitive functional dependency?
#O A) 1NF     B) 2NF     C) 3NF     D) BCNF

#Q 27|Which is NOT one of the four necessary conditions for deadlock?
#O A) Mutual exclusion     B) Hold and wait     C) Preemption     D) Circular wait

#Q 28|Which transport-layer protocol is connectionless?
#O A) TCP     B) UDP     C) IP     D) HTTP

#Q 29|In a singly linked list of n nodes, deleting the last node costs:
#O A) O(1)     B) O(log n)     C) O(n)     D) O(n squared)

#Q 30|Value of 7 AND 5 in C, using the bitwise operator?
#O A) 7     B) 5     C) 2     D) 12

#SEC Section B - English Communication (Q31 to Q40)

#Q 31|Neither the manager nor the engineers ____ available for the review.
#O A) is     B) was     C) were     D) has been

#Q 32|Synonym of METICULOUS:
#O A) careless     B) scrupulous     C) hasty     D) vague

#Q 33|Antonym of TRANSIENT:
#O A) fleeting     B) brief     C) permanent     D) mobile

#Q 34|She is adept ____ handling client escalations.
#O A) in     B) at     C) on     D) with

#Q 35|Find the error: "Each of the candidates have submitted their forms."
#O A) Each of     B) have submitted     C) their forms     D) No error

#Q 36|Passive voice of "The team will complete the migration by Friday."
#O A) The migration will be completed by the team by Friday
#O B) The migration would be completed by the team by Friday
#O C) The migration is completed by the team by Friday
#O D) The migration has been completed by the team by Friday

#Q 37|"To cut corners" means:
#O A) Take a shortcut that lowers quality     B) Negotiate hard
#O C) Finish early     D) Divide work

#Q 38|Rearrange: (P) the deployment (Q) was postponed (R) due to an unresolved (S) security finding
#O A) PQRS     B) QPRS     C) PRQS     D) SPQR

#Q 39|Indirect speech: He said, "I am reviewing the code."
#O A) He said that he is reviewing the code
#O B) He said that he was reviewing the code
#O C) He said that I was reviewing the code
#O D) He says that he was reviewing the code

#Q 40|Read the passage and answer.
#C
Automated testing reduces regression defects, but teams that rely on it
exclusively often miss usability problems. Test suites verify what
developers anticipated; they cannot report what a confused user would
experience.
#E
#P The passage implies automated testing is:
#O A) Unnecessary     B) Sufficient on its own
#O C) Limited to anticipated scenarios     D) More expensive than manual testing

#SEC Section C - Game-Based Cognitive (Q41 to Q44)

#Q 41|GeoSudo. Each row and each column contains CIR, TRI, SQR and PLS exactly once. What replaces the question mark?
#C
CIR   TRI   SQR   PLS
TRI   CIR   PLS   SQR
SQR   PLS   CIR   TRI
PLS   SQR   TRI    ?
#E
#O A) CIR     B) TRI     C) SQR     D) PLS

#Q 42|digitChallenge. Insert operators so the equation holds.
#C
5  _  3  _  2  =  13
#E
#O A) + then *     B) * then -     C) - then *     D) * then +

#Q 43|motionChallenge, discrete tick. A 4 by 4 grid. The ball starts at row 1, column 1 and the hole is at row 4, column 4. One orthogonal move per step. Cells (2,2) and (3,3) are blocked. Minimum number of steps?
#O A) 6     B) 7     C) 8     D) 3

#Q 44|Inductive reasoning. What is the next term?
#C
2,  6,  12,  20,  30,  ?
#E
#O A) 40     B) 42     C) 44     D) 36

#SEC Section D - Coding Round (45 minutes, C / C++ / Java)

#SUB Problem 1 - Second Largest Distinct Element
#P Given an integer array of size n, return the second largest distinct element. Return -1 if it does not exist. Single pass, O(n) time, O(1) extra space.
#C
Input   [12, 35, 1, 10, 34, 1]        Output   34
Input   [7, 7, 7]                     Output   -1
#E

#SUB Problem 2 - Pair Sum Count
#P Given an integer array and a target value, count the index pairs (i, j) with i less than j such that arr[i] + arr[j] equals the target. Handle duplicates correctly. O(n) time expected.
#C
Input   arr = [1, 5, 7, -1, 5], target = 6      Output   3
        pairs: 1+5, 7+(-1), 1+5
#E
"""

SET2 = r"""
#SET Test Set 2
#N Standard Analyst band.

#SEC Section A - Pseudo-code (Q1 to Q20)

#Q 1
#C
Integer a, b
Set a = 9, b = 4
a = a MOD b
b = b MOD a
Print a + b
#E
#O A) 0     B) 1     C) 5     D) 4

#Q 2
#C
Integer p, q, r
Set p = 6, q = 3, r = 2
r = (p OR q) AND (r << 1)
Print r
#E
#O A) 0     B) 4     C) 7     D) 3

#Q 3
#C
Integer i, s
Set s = 1
for(each i from 1 to 4)
  s = s * 2
End for
Print s
#E
#O A) 8     B) 16     C) 32     D) 24

#Q 4
#C
Integer fun(Integer n)
  if(n == 0)
    return 1
  End if
  return n * fun(n - 1)
End function fun()
Print fun(5) / fun(3)
#E
#O A) 20     B) 24     C) 6     D) 40

#Q 5
#C
Integer n, c
Set n = 45, c = 0
while(n > 0)
  if((n MOD 10) MOD 2 == 1)
    c = c + 1
  End if
  n = n / 10
End while
Print c
#E
#O A) 0     B) 1     C) 2     D) 45

#Q 6
#C
Integer Array[5], i, s
Set Array = {2, 4, 6, 8, 10}
Set s = 0
for(each i from 0 to 4)
  s = s + Array[i] * i
End for
Print s
#E
#O A) 60     B) 80     C) 30     D) 100

#Q 7
#C
String s
Set s = "LEVEL"
Integer i, f
Set f = 1
for(each i from 0 to LENGTH(s)/2 - 1)
  if(s[i] != s[LENGTH(s) - 1 - i])
    f = 0
  End if
End for
Print f
#E
#O A) 0     B) 1     C) 5     D) 2

#Q 8
#C
Integer x, y, z
Set x = 2, y = 3, z = 4
x = y
y = z
z = x
Print x, y, z
#E
#O A) 3 4 3     B) 2 3 4     C) 4 3 2     D) 3 4 2

#Q 9
#C
Integer a, b, i
Set a = 1, b = 1
for(each i from 1 to 5)
  a = a + b
  b = a - b
End for
Print a, b
#E
#O A) 13 8     B) 8 5     C) 21 13     D) 12 7

#Q 10
#C
Integer n, c
Set n = 100, c = 0
while(n > 0)
  n = n / 2
  c = c + 1
End while
Print c
#E
#O A) 6     B) 7     C) 8     D) 5

#Q 11
#C
Integer i, j, s
Set s = 0
for(each i from 1 to 3)
  for(each j from 1 to 3)
    if(i == j)
      s = s + i * j
    End if
  End for
End for
Print s
#E
#O A) 14     B) 6     C) 36     D) 9

#Q 12
#C
Integer Array[4], i, j, t
Set Array = {7, 3, 9, 1}
for(each i from 0 to 2)
  for(each j from 0 to 2 - i)
    if(Array[j] > Array[j+1])
      t = Array[j]
      Array[j] = Array[j+1]
      Array[j+1] = t
    End if
  End for
End for
Print Array[0], Array[3]
#E
#O A) 1 9     B) 7 1     C) 9 1     D) 3 9

#Q 13
#C
Integer a
Set a = 5
if(a > 3)
  if(a > 7)
    Print "HIGH"
  else
    Print "MID"
  End if
else
  Print "LOW"
End if
#E
#O A) HIGH     B) MID     C) LOW     D) No output

#Q 14
#C
Integer n, s
Set n = 6, s = 0
while(n != 0)
  s = s + n
  n = n - 2
End while
Print s
#E
#O A) 12     B) 21     C) 6     D) Infinite loop

#Q 15
#C
Integer x, y
Set x = 7, y = 2
Print x / y, x MOD y
#E
#O A) 3 1     B) 3.5 1     C) 3 0     D) 2 3

#Q 16
#C
String s, r
Integer i
Set s = "DATA", r = ""
for(each i from LENGTH(s) - 1 down to 0)
  r = r + s[i]
End for
Print r
#E
#O A) DATA     B) ATAD     C) AATD     D) TADA

#Q 17
#C
Integer p, q
Set p = 3, q = 5
p = p XOR q
q = p XOR q
p = p XOR q
Print p, q
#E
#O A) 5 3     B) 3 5     C) 6 3     D) 0 0

#Q 18
#C
Integer n, c
Set n = 8, c = 0
while(n > 0)
  if(n MOD 2 == 1)
    c = c + 1
  End if
  n = n / 2
End while
Print c
#E
#O A) 1     B) 3     C) 4     D) 0

#Q 19
#C
Integer Array[5], i, j, t
Set Array = {1, 2, 3, 4, 5}
Set i = 0, j = 4
while(i < j)
  t = Array[i]
  Array[i] = Array[j]
  Array[j] = t
  i = i + 1
  j = j - 1
End while
Print Array[1]
#E
#O A) 2     B) 4     C) 3     D) 1

#Q 20
#C
Integer a, b, c
Set a = 15, b = 4, c = 0
while(a >= b)
  a = a - b
  c = c + 1
End while
Print c, a
#E
#O A) 3 3     B) 4 0     C) 3 4     D) 2 7

#SEC Section A - Computer Fundamentals (Q21 to Q30)

#Q 21|Worst-case time complexity of QuickSort?
#O A) O(n log n)     B) O(n squared)     C) O(log n)     D) O(n)

#Q 22|Which is achieved through virtual functions in C++?
#O A) Compile-time polymorphism     B) Runtime polymorphism
#O C) Encapsulation     D) Overloading

#Q 23|In Java, which keyword prevents a class from being subclassed?
#O A) static     B) private     C) final     D) abstract

#Q 24|Which join returns all left-table rows plus matched right-table rows?
#O A) INNER JOIN     B) LEFT OUTER JOIN     C) RIGHT OUTER JOIN     D) CROSS JOIN

#Q 25|A queue built from two stacks: amortised dequeue cost is:
#O A) O(1)     B) O(n)     C) O(log n)     D) O(n squared)

#Q 26|Which scheduling algorithm can cause starvation?
#O A) FCFS     B) Round Robin     C) Priority scheduling     D) None

#Q 27|Default port for HTTPS?
#O A) 21     B) 80     C) 443     D) 8080

#Q 28|Which structure drives BFS traversal?
#O A) Stack     B) Queue     C) Heap     D) Linked list

#Q 29|A dangling pointer in C refers to:
#O A) A NULL address     B) Memory already freed     C) An array     D) A function

#Q 30|In ACID, the letter I stands for:
#O A) Integrity     B) Isolation     C) Indexing     D) Immutability

#SEC Section B - English Communication (Q31 to Q40)

#Q 31|The report, along with its appendices, ____ submitted yesterday.
#O A) were     B) was     C) have     D) are

#Q 32|Synonym of PRAGMATIC:
#O A) idealistic     B) practical     C) theoretical     D) reckless

#Q 33|Antonym of AUGMENT:
#O A) expand     B) diminish     C) supplement     D) enhance

#Q 34|The migration is contingent ____ client approval.
#O A) to     B) on     C) for     D) with

#Q 35|Find the error: "He suggested to postpone the release."
#O A) He suggested     B) to postpone     C) the release     D) No error

#Q 36|Active voice of "The bug was reported by the QA team."
#O A) The QA team reports the bug     B) The QA team reported the bug
#O C) The QA team has reported the bug     D) The bug reports the QA team

#Q 37|"Back to the drawing board" means:
#O A) Start planning again after failure     B) Draw diagrams
#O C) Revisit old files     D) Delegate

#Q 38|Rearrange: (P) before the sprint (Q) the backlog (R) must be groomed (S) begins
#O A) QRPS     B) PQRS     C) QRSP     D) PSQR

#Q 39|Indirect speech: She asked, "Where is the config file?"
#O A) She asked where the config file is
#O B) She asked where the config file was
#O C) She asked where was the config file
#O D) She asks where the config file was

#Q 40|Read the passage and answer.
#C
Code review catches defects, but its greater value is knowledge transfer.
A reviewer who reads unfamiliar modules acquires context that becomes
valuable when the original author leaves the team.
#E
#P The primary benefit emphasised is:
#O A) Defect detection     B) Faster releases
#O C) Distribution of knowledge     D) Reduced documentation

#SEC Section C - Game-Based Cognitive (Q41 to Q44)

#Q 41|GeoSudo. What replaces the question mark?
#C
TRI   SQR   PLS   CIR
SQR   PLS   CIR   TRI
PLS   CIR   TRI   SQR
CIR   TRI   SQR    ?
#E
#O A) CIR     B) TRI     C) SQR     D) PLS

#Q 42|digitChallenge. Insert operators so the equation holds.
#C
8  _  4  _  3  =  5
#E
#O A) / then +     B) * then -     C) - then +     D) + then /

#Q 43|Inductive reasoning. What is the next term?
#C
3,  8,  15,  24,  35,  ?
#E
#O A) 44     B) 46     C) 48     D) 50

#Q 44|switchChallenge style rule application. Switch A doubles the value. Switch B subtracts 3. Switch C halves it using integer division. Starting at 10, apply A, B, C, B in that order. Final value?
#O A) 4     B) 5     C) 7     D) 8

#SEC Section D - Coding Round (45 minutes)

#SUB Problem 1 - Move Zeros
#P Given an integer array, shift every 0 to the end while preserving the relative order of the non-zero elements. Modify the array in place. O(n) time, O(1) extra space.
#C
Input   [0, 1, 0, 3, 12]        Output   [1, 3, 12, 0, 0]
#E

#SUB Problem 2 - Longest Substring Without Repeating Characters
#P Given a string, return the length of the longest substring that contains no repeated character. Sliding window, O(n).
#C
Input   "abcabcbb"     Output   3
Input   "bbbbb"        Output   1
Input   "pwwkew"       Output   3
#E
"""

SET3 = r"""
#SET Test Set 3
#N Standard Analyst band.

#SEC Section A - Pseudo-code (Q1 to Q20)

#Q 1
#C
Integer a, b, c
Set a = 11, b = 4
c = a / b + a MOD b
Print c
#E
#O A) 5     B) 2     C) 3     D) 7

#Q 2
#C
Integer p, q
Set p = 5, q = 3
p = p << q
Print p
#E
#O A) 15     B) 40     C) 8     D) 20

#Q 3
#C
Integer i, s
Set s = 0
for(each i from 10 down to 1)
  if(i MOD 3 == 0)
    s = s + i
  End if
End for
Print s
#E
#O A) 18     B) 12     C) 21     D) 9

#Q 4
#C
Integer fun(Integer a, Integer b)
  if(b == 0)
    return 1
  End if
  return a * fun(a, b - 1)
End function fun()
Print fun(3, 4)
#E
#O A) 12     B) 27     C) 81     D) 64

#Q 5
#C
Integer n, c
Set n = 1024, c = 0
while(n > 1)
  n = n / 4
  c = c + 1
End while
Print c
#E
#O A) 4     B) 5     C) 6     D) 10

#Q 6
#C
Integer Array[6], lo, hi, mid, key, pos
Set Array = {4, 8, 15, 16, 23, 42}
Set lo = 0, hi = 5, key = 23, pos = -1
while(lo <= hi)
  mid = (lo + hi) / 2
  if(Array[mid] == key)
    pos = mid
    break
  else if(Array[mid] < key)
    lo = mid + 1
  else
    hi = mid - 1
  End if
End while
Print pos
#E
#O A) 3     B) 4     C) 5     D) -1

#Q 7
#C
String s
Integer i, c
Set s = "ENGINEER", c = 0
for(each i from 0 to LENGTH(s) - 1)
  if(s[i] == 'E')
    c = c + 1
  End if
End for
Print c
#E
#O A) 2     B) 3     C) 4     D) 8

#Q 8
#C
Integer a, b
Set a = 6, b = 2
while(b <= a)
  b = b * 2
End while
Print b
#E
#O A) 4     B) 8     C) 6     D) 16

#Q 9
#C
Integer x, y, z
Set x = 4, y = 5
if(x > y)
  z = x
else
  z = y
End if
Print z * 2
#E
#O A) 8     B) 10     C) 9     D) 20

#Q 10
#C
Integer n, s, t
Set n = 3, s = 0
for(each t from 1 to n)
  s = s + t * t * t
End for
Print s
#E
#O A) 14     B) 36     C) 27     D) 6

#Q 11
#C
Integer Array[5], i, s1, s2
Set Array = {10, 20, 30, 40, 50}
Set s1 = 0, s2 = 0
for(each i from 0 to 4)
  if(i < 2)
    s1 = s1 + Array[i]
  else
    s2 = s2 + Array[i]
  End if
End for
Print s2 - s1
#E
#O A) 60     B) 90     C) 120     D) 30

#Q 12
#C
Integer a, b, c
Set a = 2, b = 3, c = 4
a = a * b
b = b + c
c = a - b
Print a, b, c
#E
#O A) 6 7 -1     B) 6 7 1     C) 2 3 4     D) 5 7 -2

#Q 13
#C
Integer i, c
Set c = 0
for(each i from 1 to 20)
  if(i MOD 4 == 0 AND i MOD 6 == 0)
    c = c + 1
  End if
End for
Print c
#E
#O A) 0     B) 1     C) 2     D) 3

#Q 14
#C
Integer n, d, c
Set n = 1010, c = 0, d = 1
while(n > 0)
  c = c + (n MOD 10) * d
  d = d * 2
  n = n / 10
End while
Print c
#E
#O A) 10     B) 1010     C) 5     D) 2

#Q 15
#C
Integer p, q, r
Set p = 9, q = 6
r = p AND q
Print r
#E
#O A) 0     B) 15     C) 9     D) 6

#Q 16
#C
String s
Integer i, c
Set s = "aAbB", c = 0
for(each i from 0 to LENGTH(s) - 1)
  if(s[i] >= 'a' AND s[i] <= 'z')
    c = c + 1
  End if
End for
Print c
#E
#O A) 1     B) 2     C) 3     D) 4

#Q 17
#C
Integer i, j
Set j = 0
for(each i from 1 to 5)
  if(i == 3)
    continue
  End if
  j = j + i
End for
Print j
#E
#O A) 15     B) 12     C) 10     D) 6

#Q 18
#C
Integer Array[5], i, c
Set Array = {3, 3, 5, 5, 7}
Set c = 0
for(each i from 0 to 3)
  if(Array[i] == Array[i+1])
    c = c + 1
  End if
End for
Print c
#E
#O A) 1     B) 2     C) 3     D) 0

#Q 19
#C
Integer a, b, t, i
Set a = 0, b = 1
for(each i from 1 to 6)
  t = a + b
  a = b
  b = t
End for
Print a
#E
#O A) 5     B) 8     C) 13     D) 21

#Q 20
#C
Integer n, m, c
Set n = 30, m = 12, c = 1
while(m != 0)
  c = n MOD m
  n = m
  m = c
End while
Print n * 2
#E
#O A) 6     B) 12     C) 24     D) 4

#SEC Section A - Computer Fundamentals (Q21 to Q30)

#Q 21|Auxiliary space complexity of merge sort on an array of n elements?
#O A) O(1)     B) O(log n)     C) O(n)     D) O(n log n)

#Q 22|Which principle hides internal state behind an interface?
#O A) Inheritance     B) Encapsulation     C) Polymorphism     D) Composition

#Q 23|In C++, which is NOT inherited by a derived class?
#O A) public members     B) protected members     C) constructors     D) member functions

#Q 24|Which statement removes all rows, keeps the table structure, and in most DBMSs cannot be rolled back?
#O A) DELETE     B) DROP     C) TRUNCATE     D) ALTER

#Q 25|Maximum nodes in a binary tree of height h, with the root at height 0?
#O A) 2 to the power h     B) 2 to the power (h+1), minus 1
#O C) 2h + 1     D) h squared

#Q 26|Thrashing in an operating system is caused by:
#O A) Excessive page faults     B) CPU overheating     C) Deadlock     D) Disk fragmentation

#Q 27|Which OSI layer handles routing?
#O A) Data link     B) Network     C) Transport     D) Session

#Q 28|Which BST traversal yields sorted order?
#O A) Preorder     B) Inorder     C) Postorder     D) Level order

#Q 29|In Java, the mutable and non-thread-safe alternative to String is:
#O A) StringBuffer     B) StringBuilder     C) CharArray     D) StringJoiner

#Q 30|A candidate key not chosen as the primary key is called:
#O A) Foreign key     B) Alternate key     C) Super key     D) Composite key

#SEC Section B - English Communication (Q31 to Q40)

#Q 31|Not only the developers but also the architect ____ present at the demo.
#O A) were     B) are     C) was     D) have been

#Q 32|Synonym of SUCCINCT:
#O A) verbose     B) concise     C) elaborate     D) hesitant

#Q 33|Antonym of OBSOLETE:
#O A) outdated     B) archaic     C) current     D) rare

#Q 34|They complied ____ the new security policy.
#O A) to     B) with     C) on     D) for

#Q 35|Find the error: "The number of open tickets have increased sharply."
#O A) The number of     B) have increased     C) sharply     D) No error

#Q 36|Passive of "Someone has deleted the log files."
#O A) The log files have been deleted     B) The log files were deleted
#O C) The log files are deleted     D) The log files had been deleted

#Q 37|"In the loop" means:
#O A) Stuck repeating     B) Kept informed     C) Writing loops     D) Out of scope

#Q 38|Rearrange: (P) unless the root cause (Q) the incident (R) is identified (S) will recur
#O A) PRQS     B) QSPR     C) PQRS     D) QRPS

#Q 39|Indirect speech: The lead said, "We deployed the patch last night."
#O A) The lead said that they deployed the patch last night
#O B) The lead said that they had deployed the patch the previous night
#O C) The lead said that we had deployed the patch last night
#O D) The lead says that they deployed the patch last night

#Q 40|Read the passage and answer.
#C
Microservices reduce coupling between teams but increase operational
surface area. An organisation without mature monitoring often trades a
manageable monolith for a distributed system it cannot observe.
#E
#P The author's caution is that microservices:
#O A) Always perform worse     B) Require operational maturity to pay off
#O C) Eliminate coupling entirely     D) Are cheaper to run

#SEC Section C - Game-Based Cognitive (Q41 to Q44)

#Q 41|GeoSudo. What replaces the question mark?
#C
PLS   CIR   TRI   SQR
CIR   TRI   SQR   PLS
TRI   SQR   PLS   CIR
SQR   PLS   CIR    ?
#E
#O A) CIR     B) TRI     C) SQR     D) PLS

#Q 42|digitChallenge. Insert operators so the equation holds.
#C
6  _  2  _  7  =  5
#E
#O A) / then +     B) * then -     C) + then -     D) - then *

#Q 43|Inductive reasoning. What is the next term?
#C
5,  11,  23,  47,  ?
#E
#O A) 89     B) 92     C) 94     D) 95

#Q 44|Rule application. Switch X adds 5. Switch Y multiplies by 3. Starting at 4, apply Y, X, Y in that order. Final value?
#O A) 27     B) 39     C) 51     D) 57

#SEC Section D - Coding Round (45 minutes)

#SUB Problem 1 - Remove Duplicates from Sorted Array
#P Given a sorted array, remove duplicates in place so each element appears once, and return the new length. Elements beyond the returned length do not matter. O(n) time, O(1) space.
#C
Input   [1, 1, 2, 2, 2, 3, 4, 4]
Output  4, and the array begins [1, 2, 3, 4]
#E

#SUB Problem 2 - Maximum Subarray Sum
#P Given an integer array that may contain negatives, return the largest sum obtainable from any contiguous non-empty subarray. O(n) single pass.
#C
Input   [-2, 1, -3, 4, -1, 2, 1, -5, 4]     Output   6
Input   [-3, -1, -7]                        Output   -1
#E
"""

SET4 = r"""
#SET Test Set 4
#N Standard Analyst band.

#SEC Section A - Pseudo-code (Q1 to Q20)

#Q 1
#C
Integer a, b
Set a = 13, b = 5
Print a MOD b, a / b
#E
#O A) 3 2     B) 2 3     C) 3 2.6     D) 2 3.0

#Q 2
#C
Integer p
Set p = 40
p = p >> 2
p = p << 1
Print p
#E
#O A) 40     B) 20     C) 10     D) 80

#Q 3
#C
Integer i, s
Set s = 0
for(each i from 1 to 5)
  s = s + i * (i + 1)
End for
Print s
#E
#O A) 55     B) 70     C) 30     D) 45

#Q 4
#C
Integer fun(Integer n)
  if(n < 2)
    return n
  End if
  return fun(n / 2) + (n MOD 2)
End function fun()
Print fun(13)
#E
#O A) 2     B) 3     C) 4     D) 13

#Q 5
#C
Integer n, c
Set n = 7, c = 0
while(n != 1)
  if(n MOD 2 == 0)
    n = n / 2
  else
    n = 3 * n + 1
  End if
  c = c + 1
End while
Print c
#E
#O A) 11     B) 16     C) 17     D) 7

#Q 6
#C
Integer Array[6], i, mx, mn
Set Array = {5, 2, 9, 1, 7, 3}
Set mx = Array[0], mn = Array[0]
for(each i from 1 to 5)
  if(Array[i] > mx)
    mx = Array[i]
  End if
  if(Array[i] < mn)
    mn = Array[i]
  End if
End for
Print mx - mn
#E
#O A) 8     B) 9     C) 6     D) 4

#Q 7
#C
String s
Integer i, c
Set s = "SUCCESS", c = 0
for(each i from 0 to LENGTH(s) - 2)
  if(s[i] == s[i+1])
    c = c + 1
  End if
End for
Print c
#E
#O A) 1     B) 2     C) 3     D) 4

#Q 8
#C
Integer a, b, c
Set a = 1, b = 2, c = 3
if(a < b AND b < c)
  Print a + c
else
  Print a - c
End if
#E
#O A) -2     B) 4     C) 6     D) 3

#Q 9
#C
Integer n, s, i, j
Set n = 5, s = 0
for(each i from 1 to n)
  for(each j from 1 to i)
    s = s + 1
  End for
End for
Print s
#E
#O A) 15     B) 25     C) 10     D) 5

#Q 10
#C
Integer Array[5], i, minIdx, t
Set Array = {2, 4, 1, 5, 3}
Set minIdx = 0
for(each i from 1 to 4)
  if(Array[i] < Array[minIdx])
    minIdx = i
  End if
End for
t = Array[0]
Array[0] = Array[minIdx]
Array[minIdx] = t
Print Array[0], Array[2]
#E
#O A) 1 2     B) 2 1     C) 1 4     D) 2 4

#Q 11
#C
Integer x, i
Set x = 0
for(each i from 1 to 4)
  x = x * 10 + i
End for
Print x
#E
#O A) 1234     B) 10     C) 4321     D) 4

#Q 12
#C
Integer a, b
Set a = 17, b = 5
a = a - (a MOD b)
Print a
#E
#O A) 15     B) 12     C) 17     D) 2

#Q 13
#C
Integer p, q, r
Set p = 1, q = 2, r = 0
r = (p XOR q) OR (r OR 1)
Print r
#E
#O A) 1     B) 2     C) 3     D) 0

#Q 14
#C
Integer n, c
Set n = 6, c = 1
while(n > 0)
  c = c * n
  n = n - 2
End while
Print c
#E
#O A) 48     B) 720     C) 12     D) 24

#Q 15
#C
String s1, s2
Integer i, f
Set s1 = "abc", s2 = "cba", f = 1
for(each i from 0 to 2)
  if(s1[i] != s2[2 - i])
    f = 0
  End if
End for
Print f
#E
#O A) 0     B) 1     C) 3     D) 2

#Q 16
#C
Integer i, j, c
Set c = 0, i = 1
while(i <= 4)
  Set j = 1
  while(j <= i)
    c = c + j
    j = j + 1
  End while
  i = i + 1
End while
Print c
#E
#O A) 20     B) 10     C) 16     D) 24

#Q 17
#C
Integer Array[4], i, d, v
Set Array = {1, 0, 1, 1}
Set v = 0, d = 1
for(each i from 3 down to 0)
  v = v + Array[i] * d
  d = d * 2
End for
Print v
#E
#O A) 11     B) 13     C) 7     D) 1011

#Q 18
#C
Integer n, s
Set n = 234, s = 0
while(n > 0)
  s = s * 10 + (n MOD 10)
  n = n / 10
End while
if(s > 234)
  Print "GREATER"
else
  Print "NOT GREATER"
End if
#E
#O A) GREATER     B) NOT GREATER     C) 432     D) 234

#Q 19
#C
Integer i, c
Set c = 0
for(each i from 2 to 10)
  if(i MOD 2 == 0 OR i MOD 5 == 0)
    c = c + 1
  End if
End for
Print c
#E
#O A) 5     B) 6     C) 7     D) 4

#Q 20
#C
Integer Array[5], i, j, t
Set Array = {9, 7, 5, 3, 1}
for(each i from 0 to 1)
  for(each j from 0 to 3 - i)
    if(Array[j] > Array[j+1])
      t = Array[j]
      Array[j] = Array[j+1]
      Array[j+1] = t
    End if
  End for
End for
Print Array[0], Array[4]
#E
#O A) 5 9     B) 1 9     C) 9 1     D) 3 9

#SEC Section A - Computer Fundamentals (Q21 to Q30)

#Q 21|In C, given int a = 5; int b = a++; int c = ++a; what are b and c?
#O A) 5 6     B) 5 7     C) 6 7     D) 6 6

#Q 22|Which sort is stable with O(n log n) worst case?
#O A) QuickSort     B) Merge sort     C) Heap sort     D) Selection sort

#Q 23|Which Java collection disallows duplicates?
#O A) ArrayList     B) LinkedList     C) HashSet     D) Vector

#Q 24|SQL DISTINCT does what?
#O A) Sorts rows     B) Removes duplicate rows from the result
#O C) Joins tables     D) Filters groups

#Q 25|Best case time complexity of insertion sort?
#O A) O(1)     B) O(n)     C) O(n log n)     D) O(n squared)

#Q 26|Where are non-static local variables stored in C?
#O A) Heap     B) Stack     C) Data segment     D) Text segment

#Q 27|ARP resolves:
#O A) Domain name to IP     B) IP to MAC     C) MAC to IP     D) Port to process

#Q 28|Which gives O(1) average lookup by key?
#O A) Array     B) Linked list     C) Hash table     D) BST

#Q 29|An abstract class:
#O A) Can be instantiated directly
#O B) Cannot be instantiated and may contain abstract methods
#O C) Must contain only abstract methods     D) Cannot have constructors

#Q 30|Reading data written by an uncommitted transaction is a:
#O A) Phantom read     B) Dirty read     C) Lost update     D) Non-repeatable read

#SEC Section B - English Communication (Q31 to Q40)

#Q 31|Each of the modules ____ its own test suite.
#O A) have     B) has     C) are having     D) were having

#Q 32|Synonym of ROBUST:
#O A) fragile     B) resilient     C) sluggish     D) minimal

#Q 33|Antonym of REDUNDANT:
#O A) superfluous     B) essential     C) excessive     D) repetitive

#Q 34|The outage was attributed ____ a misconfigured load balancer.
#O A) on     B) to     C) for     D) with

#Q 35|Find the error: "Neither of the two approaches are viable."
#O A) Neither of     B) the two approaches     C) are viable     D) No error

#Q 36|Passive of "The architect will review the design tomorrow."
#O A) The design will be reviewed by the architect tomorrow
#O B) The design is reviewed by the architect tomorrow
#O C) The design was reviewed by the architect tomorrow
#O D) The design would be reviewed by the architect tomorrow

#Q 37|"Low-hanging fruit" means:
#O A) Easy wins     B) Unripe work     C) Low priority     D) Cheap tools

#Q 38|Rearrange: (P) after the schema change (Q) the reports (R) were regenerated (S) had been applied
#O A) PSQR     B) QRPS     C) PQRS     D) QPRS

#Q 39|Indirect speech: She said, "I will send the report tomorrow."
#O A) She said that she will send the report tomorrow
#O B) She said that she would send the report the next day
#O C) She said that she sent the report tomorrow
#O D) She says she would send the report tomorrow

#Q 40|Read the passage and answer.
#C
Technical debt is not a defect. It is a deliberate trade-off taken to ship
sooner, and it becomes a problem only when teams stop tracking what they
borrowed.
#E
#P Technical debt turns harmful when:
#O A) It is incurred at all     B) It goes unrecorded
#O C) Releases are delayed     D) Code is refactored

#SEC Section C - Game-Based Cognitive (Q41 to Q44)

#Q 41|GeoSudo. What replaces the question mark?
#C
CIR   PLS   SQR   TRI
PLS   SQR   TRI   CIR
SQR   TRI   CIR   PLS
TRI   CIR   PLS    ?
#E
#O A) CIR     B) TRI     C) SQR     D) PLS

#Q 42|digitChallenge. Place 3, 4 and 6 into the blanks so the equation holds. Each digit is used once.
#C
_  +  _  *  _  =  27
#E
#O A) 3, 4, 6     B) 4, 3, 6     C) 6, 4, 3     D) 4, 6, 3

#Q 43|Inductive reasoning. What is the next term?
#C
2,  5,  10,  17,  26,  ?
#E
#O A) 35     B) 36     C) 37     D) 38

#Q 44|motionChallenge, discrete tick. A 5 by 5 grid. The ball starts at row 1, column 1 and the hole is at row 5, column 5. One orthogonal move per step. Cells (1,3), (2,3), (3,3) and (4,3) are blocked. Minimum number of steps?
#O A) 8     B) 9     C) 10     D) 12

#SEC Section D - Coding Round (45 minutes)

#SUB Problem 1 - Anagram Check
#P Given two strings, determine whether they are anagrams of each other. Case-sensitive. Return true or false. O(n) time.
#C
Input   "listen", "silent"      Output   true
Input   "hello", "world"        Output   false
#E

#SUB Problem 2 - Balanced Parentheses
#P Given a string containing only the six bracket characters, determine whether every bracket is closed by the correct type in the correct order. Use a stack. O(n) time.
#C
Input   "{[()]}"      Output   true
Input   "{[(])}"      Output   false
Input   "((("         Output   false
#E
"""

SET5 = r"""
#SET Test Set 5
#N Standard Analyst band.

#SEC Section A - Pseudo-code (Q1 to Q20)

#Q 1
#C
Integer a, b, c
Set a = 25, b = 7
c = (a / b) * b + (a MOD b)
Print c
#E
#O A) 21     B) 25     C) 4     D) 28

#Q 2
#C
Integer p, q
Set p = 1, q = 6
p = p << q
p = p >> 3
Print p
#E
#O A) 8     B) 64     C) 16     D) 2

#Q 3
#C
Integer i, s
Set s = 0
for(each i from 1 to 9)
  if(i MOD 2 == 1)
    s = s + i
  End if
End for
Print s
#E
#O A) 20     B) 25     C) 45     D) 24

#Q 4
#C
Integer fun(Integer n)
  if(n <= 0)
    return 0
  End if
  return n + fun(n - 3)
End function fun()
Print fun(10)
#E
#O A) 22     B) 25     C) 18     D) 10

#Q 5
#C
Integer n, c
Set n = 3125, c = 0
while(n MOD 5 == 0)
  n = n / 5
  c = c + 1
End while
Print c
#E
#O A) 4     B) 5     C) 6     D) 3

#Q 6
#C
Integer Array[7], lo, hi, mid, key, c
Set Array = {1, 3, 5, 7, 9, 11, 13}
Set lo = 0, hi = 6, key = 4, c = 0
while(lo <= hi)
  mid = (lo + hi) / 2
  c = c + 1
  if(Array[mid] == key)
    break
  else if(Array[mid] < key)
    lo = mid + 1
  else
    hi = mid - 1
  End if
End while
Print c
#E
#O A) 2     B) 3     C) 4     D) 7

#Q 7
#C
String s
Integer i, c
Set s = "MISSISSIPPI", c = 0
for(each i from 0 to LENGTH(s) - 1)
  if(s[i] == 'S')
    c = c + 1
  End if
End for
Print c
#E
#O A) 2     B) 3     C) 4     D) 5

#Q 8
#C
Integer a, b, c
Set a = 2, b = 10, c = 0
while(a < b)
  a = a * 2
  b = b + 1
  c = c + 1
End while
Print c
#E
#O A) 2     B) 3     C) 4     D) Infinite loop

#Q 9
#C
Integer x, y
Set x = 8, y = 3
if(x MOD y == 0)
  Print "DIVISIBLE"
else if(x > y * 2)
  Print "LARGE"
else
  Print "SMALL"
End if
#E
#O A) DIVISIBLE     B) LARGE     C) SMALL     D) No output

#Q 10
#C
Integer n, s, i
Set n = 4, s = 0
for(each i from 1 to n)
  s = s + (n - i + 1)
End for
Print s
#E
#O A) 10     B) 4     C) 16     D) 6

#Q 11
#C
Integer Array[6], i, x
Set Array = {4, 4, 2, 2, 6, 6}
Set x = 0
for(each i from 0 to 5)
  x = x XOR Array[i]
End for
Print x
#E
#O A) 0     B) 4     C) 24     D) 6

#Q 12
#C
Integer a, b, c
Set a = 7, b = 7
if(a == b)
  c = a * b
else
  c = a + b
End if
Print c MOD 10
#E
#O A) 4     B) 9     C) 49     D) 14

#Q 13
#C
Integer i, j, s
Set s = 0
for(each i from 1 to 3)
  for(each j from 3 down to 1)
    if(i + j == 4)
      s = s + 1
    End if
  End for
End for
Print s
#E
#O A) 2     B) 3     C) 4     D) 9

#Q 14
#C
Integer n, r
Set n = 1234, r = 0
while(n > 0)
  if((n MOD 10) MOD 2 == 0)
    r = r + (n MOD 10)
  End if
  n = n / 10
End while
Print r
#E
#O A) 4     B) 6     C) 10     D) 2

#Q 15
#C
String s
Integer i
Set s = "ABCD"
for(each i from 0 to LENGTH(s) - 1)
  if(i MOD 2 == 0)
    Print s[i]
  End if
End for
#E
#O A) AC     B) BD     C) ABCD     D) DCBA

#Q 16
#C
Integer a, b, t
Set a = 48, b = 18
while(b != 0)
  t = b
  b = a MOD b
  a = t
End while
Print a
#E
#O A) 6     B) 12     C) 18     D) 3

#Q 17
#C
Integer Array[5], i, s
Set Array = {1, 2, 3, 4, 5}
Set s = 0
for(each i from 0 to 4)
  if(Array[i] MOD 2 == 0)
    s = s + Array[i]
  else
    s = s - Array[i]
  End if
End for
Print s
#E
#O A) 3     B) -3     C) 15     D) 6

#Q 18
#C
Integer p, q, r, i
Set p = 10, q = 3, r = 1
for(each i from 1 to q)
  r = r * p
End for
Print r / 100
#E
#O A) 10     B) 100     C) 1000     D) 1

#Q 19
#C
Integer n, c
Set n = 255, c = 0
while(n > 0)
  c = c + (n AND 1)
  n = n >> 1
End while
Print c
#E
#O A) 7     B) 8     C) 255     D) 1

#Q 20
#C
Integer Array[5], i, j, c
Set Array = {1, 2, 3, 4, 5}
Set c = 0
for(each i from 0 to 4)
  for(each j from i + 1 to 4)
    if(Array[i] + Array[j] == 6)
      c = c + 1
    End if
  End for
End for
Print c
#E
#O A) 1     B) 2     C) 3     D) 4

#SEC Section A - Computer Fundamentals (Q21 to Q30)

#Q 21|Inserting at the head of a singly linked list costs:
#O A) O(1)     B) O(n)     C) O(log n)     D) O(n squared)

#Q 22|Which C++ feature lets an operator work with user-defined types?
#O A) Templates     B) Operator overloading     C) Friend functions     D) Virtual inheritance

#Q 23|In Java, if a class declares no constructor:
#O A) Compile error     B) The compiler supplies a no-argument default constructor
#O C) The class cannot be instantiated     D) Runtime error

#Q 24|Which ignores NULL values?
#O A) COUNT(*)     B) COUNT(column)     C) Both     D) Neither

#Q 25|Height of a balanced BST with n nodes?
#O A) O(n)     B) O(log n)     C) O(1)     D) O(n log n)

#Q 26|Which page replacement algorithm can exhibit Belady's anomaly?
#O A) LRU     B) FIFO     C) Optimal     D) LFU

#Q 27|DNS uses which transport protocol for standard queries?
#O A) TCP     B) UDP     C) ICMP     D) ARP

#Q 28|Which structure implements recursion internally?
#O A) Queue     B) Stack     C) Heap     D) Graph

#Q 29|In C, malloc returns:
#O A) An int     B) A void pointer     C) A char pointer     D) The allocated size

#Q 30|Which dependency does 2NF eliminate?
#O A) Transitive     B) Partial     C) Multivalued     D) Join

#SEC Section B - English Communication (Q31 to Q40)

#Q 31|A set of guidelines ____ been published for the new API.
#O A) have     B) has     C) are     D) were

#Q 32|Synonym of MITIGATE:
#O A) worsen     B) alleviate     C) ignore     D) accelerate

#Q 33|Antonym of VOLATILE:
#O A) unstable     B) stable     C) erratic     D) explosive

#Q 34|The team is averse ____ changing the release date.
#O A) of     B) to     C) for     D) with

#Q 35|Find the error: "He is one of the engineers who has contributed to the framework."
#O A) He is one of     B) the engineers     C) who has contributed     D) No error

#Q 36|Passive of "They are testing the new build."
#O A) The new build is being tested     B) The new build was tested
#O C) The new build has been tested     D) The new build is tested

#Q 37|"Move the needle" means:
#O A) Make a noticeable difference     B) Adjust settings
#O C) Delay     D) Measure precisely

#Q 38|Rearrange: (P) the release notes (Q) once the build passes (R) will be published (S) regression testing
#O A) QSPR     B) PQRS     C) QPRS     D) PRQS

#Q 39|Indirect speech: The manager asked, "Have you closed the ticket?"
#O A) The manager asked if I had closed the ticket
#O B) The manager asked have you closed the ticket
#O C) The manager asked if I have closed the ticket
#O D) The manager asks if I closed the ticket

#Q 40|Read the passage and answer.
#C
Adding engineers to a late project rarely speeds it up. New members consume
the time of those already productive, and communication paths grow faster
than headcount.
#E
#P The central claim rests on:
#O A) New engineers lacking skill     B) Coordination cost rising non-linearly
#O C) Budget constraints     D) Poor documentation

#SEC Section C - Game-Based Cognitive (Q41 to Q44)

#Q 41|GeoSudo. What replaces the question mark?
#C
SQR   TRI   CIR   PLS
TRI   CIR   PLS   SQR
CIR   PLS   SQR   TRI
PLS   SQR   TRI    ?
#E
#O A) CIR     B) TRI     C) SQR     D) PLS

#Q 42|digitChallenge. Insert operators so the equation holds.
#C
20  _  5  _  3  =  1
#E
#O A) / then -     B) - then /     C) / then +     D) * then -

#Q 43|Inductive reasoning. What is the next term?
#C
1,  2,  6,  24,  120,  ?
#E
#O A) 600     B) 620     C) 720     D) 840

#Q 44|Rule application. Button P adds 7. Button Q multiplies by 2. Button R subtracts 4. Starting at 3, apply Q, P, Q, R in that order. Final value?
#O A) 18     B) 20     C) 22     D) 26

#SEC Section D - Coding Round (45 minutes)

#SUB Problem 1 - Missing Number
#P An array holds n distinct integers drawn from the range 1 to n+1, with exactly one value missing. Return the missing value. O(n) time, O(1) space. Do not sort.
#C
Input   [1, 2, 4, 5, 6]     Output   3
Input   [2, 3, 4]           Output   1
#E

#SUB Problem 2 - Rotate Matrix 90 Degrees Clockwise
#P Given an n by n integer matrix, rotate it 90 degrees clockwise in place. No second matrix is allowed.
#C
Input        Output
1 2 3        7 4 1
4 5 6        8 5 2
7 8 9        9 6 3
#E
"""

HDIV = r"""
#PART Part Two - Senior Analyst Band
#P Sets H1 to H5 sit deliberately above Sets 1 to 5. They target the Senior Analyst gate, the track carrying the higher package, and they draw on multi-dimensional arrays, recursion with non-obvious base cases, bit manipulation, two-pointer partitioning, pass-by-value semantics, and layered switchChallenge operators.
#P On these five sets, 55 to 65 percent on Section A is a solid result for a well-prepared candidate. Scoring above 80 percent means you are comfortably past what the live assessment demands and the remaining gain is in speed rather than content.
#P Section C now uses the full Aon smartPredict format set: switchChallenge at one, two and three operator layers, digitChallenge with the digit-distinctness rule, gridChallenge with memory rounds separated by spatial distractors, and motionChallenge as discrete-tick reflection tracking. Review the notation reference at the front of this book before attempting them.
#P Timing per set: Section A 30 minutes, Section B 10 minutes, Section C 10 minutes, Section D 45 minutes.
"""

SETH1 = r"""
#SET Test Set H1
#N Senior Analyst band - medium to hard.

#SEC Section A - Pseudo-code (Q1 to Q20)

#Q 1
#C
Integer a, b, c
Set a = 2, b = 3, c = 4
a = c / b * a + b MOD a
Print a
#E
#O A) 4     B) 2     C) 3     D) 5

#Q 2
#C
Integer fun(Integer n)
  if(n == 0)
    return 0
  End if
  Print n MOD 2
  return fun(n / 2)
End function fun()
Call fun(13)
#E
#O A) 1011     B) 1101     C) 1010     D) 0111

#Q 3
#C
Integer i, c
Set c = 0, i = 1
while(i < 30)
  if(i MOD 3 == 0)
    i = i + 5
  else
    i = i + 2
  End if
  c = c + 1
End while
Print i, c
#E
#O A) 28 9     B) 30 10     C) 30 9     D) 31 10

#Q 4
#C
Integer M[3][3], i, s
Set M = {{1,2,3},{4,5,6},{7,8,9}}
Set s = 0
for(each i from 0 to 2)
  s = s + M[i][2 - i] - M[i][i]
End for
Print s
#E
#O A) 15     B) 30     C) 4     D) 0

#Q 5
#C
Integer a, b, c
Set a = 4, b = 0, c = 0
while(b < 3 AND a > b)
  b = b + 1
  a = a - 1
  c = c + a + b
End while
Print c
#E
#O A) 12     B) 8     C) 4     D) 10

#Q 6
#C
Integer modify(Integer x)
  x = x * 2
  return x + 1
End function modify()
Integer n, r
Set n = 5
r = modify(n)
Print n, r
#E
#O A) 10 11     B) 5 10     C) 5 11     D) 10 21

#Q 7
#C
String s
Integer i, c
Set s = "ABCDEFG", c = 0
for(each i from 0 to LENGTH(s) - 1)
  if((i + s[i] - 'A') MOD 3 == 0)
    c = c + 1
  End if
End for
Print c
#E
#O A) 2     B) 3     C) 4     D) 7

#Q 8
#C
Integer A[4][4], i, j, f, r
Set A = {{1,2,3,4},{5,6,7,8},{9,10,11,12},{13,14,15,16}}
Set f = 0, r = -1
for(each i from 0 to 3)
  for(each j from 0 to 3)
    if(A[i][j] MOD 7 == 0)
      r = i * 4 + j
      f = 1
      break
    End if
  End for
  if(f == 1)
    break
  End if
End for
Print r
#E
#O A) 6     B) 7     C) 14     D) 5

#Q 9
#C
Integer f(Integer n)
  if(n <= 2)
    return 1
  End if
  return f(n - 1) + f(n - 3)
End function f()
Print f(7)
#E
#O A) 6     B) 7     C) 9     D) 13

#Q 10
#C
Integer n, m, c
Set n = 45, m = 0, c = 0
while(n > 0)
  if((n AND 1) == 1)
    m = m OR (1 << c)
  End if
  n = n >> 1
  c = c + 1
End while
Print m, c
#E
#O A) 45 5     B) 45 6     C) 90 6     D) 0 6

#Q 11
#C
Integer n, s
Set n = 0, s = 0
repeat
  n = n + 3
  s = s + n
until(s > 20)
Print n, s
#E
#O A) 9 18     B) 12 18     C) 15 45     D) 12 30

#Q 12
#C
Integer A[5], i
Set A = {2, 3, 1, 5, 4}
for(each i from 1 to 4)
  A[i] = A[i] + A[i-1]
End for
Print A[2], A[4]
#E
#O A) 6 15     B) 4 15     C) 6 9     D) 1 4

#Q 13
#C
Integer A[4], i, j
Set A = {1, 2, 3, 4}
for(each i from 0 to 3)
  j = 3 - i
  A[i] = A[i] XOR A[j]
  A[j] = A[i] XOR A[j]
  A[i] = A[i] XOR A[j]
End for
Print A[0], A[1], A[2], A[3]
#E
#O A) 4 3 2 1     B) 1 2 3 4     C) 4 2 3 1     D) 0 0 0 0

#Q 14
#C
Integer x, y, r
Set x = 7, y = 12
if(x MOD 2 == 1 AND y MOD 2 == 0)
  r = x * y
else if(x + y > 15)
  r = x + y
else
  r = y - x
End if
Print r MOD 11
#E
#O A) 5     B) 8     C) 7     D) 4

#Q 15
#C
Integer i, j, c
Set c = 0
for(each i from 1 to 4)
  for(each j from 1 to 4)
    if((i * j) MOD 2 == 0 AND i != j)
      c = c + 1
    End if
  End for
End for
Print c
#E
#O A) 8     B) 10     C) 12     D) 6

#Q 16
#C
Integer n, r, d
Set n = 897, r = 0
while(n > 0)
  d = n MOD 10
  if(d MOD 3 == 0)
    r = r * 10 + (d / 3)
  else
    r = r * 10 + d
  End if
  n = n / 10
End while
Print r
#E
#O A) 798     B) 837     C) 873     D) 738

#Q 17
#C
Integer A[6], i, j, t
Set A = {3, 8, 2, 9, 1, 7}
Set i = 0, j = 5
while(i < j)
  while(i < j AND A[i] MOD 2 == 1)
    i = i + 1
  End while
  while(i < j AND A[j] MOD 2 == 0)
    j = j - 1
  End while
  if(i < j)
    t = A[i]
    A[i] = A[j]
    A[j] = t
  End if
End while
Print A[0], A[1], A[2]
#E
#O A) 3 7 1     B) 3 8 2     C) 3 7 9     D) 1 7 3

#Q 18
#C
String f(Integer n)
  if(n == 0)
    return ""
  End if
  return f(n / 2) + (n MOD 2)
End function f()
Print f(11)
#E
#O A) 1101     B) 1011     C) 11     D) 1010

#Q 19
#C
Integer M[3][3], i, j, t, s
Set M = {{1,2,3},{4,5,6},{7,8,9}}
for(each i from 0 to 2)
  for(each j from i + 1 to 2)
    t = M[i][j]
    M[i][j] = M[j][i]
    M[j][i] = t
  End for
End for
Set s = 0
for(each j from 0 to 2)
  s = s + M[0][j]
End for
Print s
#E
#O A) 6     B) 18     C) 12     D) 15

#Q 20
#C
Integer n, i, c
Set n = 100, c = 0, i = 2
while(i * i <= n)
  if(n MOD i == 0)
    c = c + 1
    while(n MOD i == 0)
      n = n / i
    End while
  End if
  i = i + 1
End while
if(n > 1)
  c = c + 1
End if
Print c
#E
#O A) 3     B) 2     C) 4     D) 1

#SEC Section A - Computer Fundamentals (Q21 to Q30)

#Q 21|An outer loop runs i from 1 to n. Inside it, j is reset to 1 and a while loop doubles j until j is no longer less than n. Total complexity?
#O A) O(n)     B) O(n log n)     C) O(n squared)     D) O(log n)

#Q 22|In C++, deleting a derived object through a base pointer when the base destructor is not virtual causes:
#O A) A compile error
#O B) Undefined behaviour - the derived destructor is not invoked
#O C) A leak confined to the base part     D) Nothing

#Q 23|Which C++ mechanism resolves the diamond problem?
#O A) Friend classes     B) Templates     C) Virtual inheritance     D) Namespaces

#Q 24|Which isolation level permits phantom reads but prevents dirty and non-repeatable reads?
#O A) Read Uncommitted     B) Read Committed     C) Repeatable Read     D) Serializable

#Q 25|Hash table with separate chaining, n keys and m buckets. Average search cost is:
#O A) O(1) unconditionally     B) O(n)     C) O(1 + n/m)     D) O(log n)

#Q 26|Breaking which single condition guarantees no deadlock?
#O A) Mutual exclusion     B) Circular wait     C) Bounded buffer     D) Fairness

#Q 27|T(n) = T(n-1) + O(1) with T(1) = O(1) describes:
#O A) O(log n)     B) O(n)     C) O(n log n)     D) O(2 to the power n)

#Q 28|In a B+ tree, where do the data records or pointers to them reside?
#O A) All nodes equally     B) Internal nodes only     C) Leaf nodes only     D) The root

#Q 29|The volatile keyword in C tells the compiler:
#O A) The variable is constant     B) Not to optimise away reads of the variable
#O C) To place it on the heap     D) To make access atomic

#Q 30|Which traversal, paired with inorder, reconstructs a binary tree uniquely?
#O A) Level order only     B) Preorder or postorder     C) Neither     D) Inorder repeated

#SEC Section B - English Communication (Q31 to Q38)

#Q 31|The committee, whose members ____ divided on the proposal, ____ yet to issue a recommendation.
#O A) is / are     B) are / has     C) are / is     D) is / is

#Q 32|Synonym of PERFUNCTORY:
#O A) thorough     B) cursory     C) enthusiastic     D) deliberate

#Q 33|Antonym of INTRANSIGENT:
#O A) stubborn     B) accommodating     C) rigid     D) hostile

#Q 34|"Hoist with one's own petard" means:
#O A) Harmed by one's own scheme     B) Promoted unexpectedly
#O C) Raising a flag     D) Abandoning a plan

#Q 35|Find the error: "Hardly had the deployment finished than the alerts began firing."
#O A) Hardly had     B) the deployment finished     C) than the alerts     D) No error

#Q 36|Which sentence has correct parallel structure?
#O A) The tool validates input, logs errors, and it retries failed calls
#O B) The tool validates input, logs errors, and retries failed calls
#O C) The tool validates input, error logging, and retrying failed calls
#O D) The tool is validating input, logs errors, and retried failed calls

#Q 37|Rearrange: (P) had the rollback been scripted (Q) the outage (R) by more than an hour (S) would have been shortened
#O A) PQSR     B) QSRP     C) PQRS     D) QPSR

#Q 38|Read the passage and answer.
#C
Advocates of formal verification note that testing can only demonstrate the
presence of defects, never their absence. Critics reply that a proof
establishes correctness relative to a specification, and specifications are
themselves written by humans. Neither camp disputes the other's premise.
#E
#P The final sentence implies the disagreement concerns:
#O A) Whether testing finds defects
#O B) Where the residual risk sits, not whether it exists
#O C) The cost of verification     D) The accuracy of proofs

#SEC Section C - Game-Based Cognitive (Q39 to Q44)

#Q 39|switchChallenge, single operator. The operator's k-th digit names which input position supplies output position k. Find the operator.
#C
Input     STR   CIR   TRI   SQR
Output    TRI   STR   SQR   CIR
#E
#O A) 2413     B) 3142     C) 3124     D) 4132

#Q 40|switchChallenge, two layers. Operator 1 is given. Find the missing Operator 2.
#C
Input         STR   CIR   TRI   SQR
Operator 1    2431
Intermediate  (hidden)
Operator 2    ?
Output        STR   TRI   CIR   SQR
#E
#O A) 3421     B) 4132     C) 4312     D) 2143

#Q 41|switchChallenge, three layers. Operators 1 and 3 are given. Find the missing middle operator.
#C
Input         STR   CIR   TRI   SQR
Operator 1    3142
Operator 2    ?
Operator 3    2143
Output        STR   CIR   SQR   TRI
#E
#O A) 4213     B) 2431     C) 4123     D) 1342

#Q 42|digitChallenge. Fill the blanks with digits 1 to 9. Each digit may be used only once in the equation. Standard precedence applies.
#C
_  *  _  -  _  /  _  =  20
#E
#O A) 4, 6, 8, 2     B) 7, 3, 2, 2     C) 3, 8, 6, 2     D) 9, 2, 4, 1

#Q 43|gridChallenge. Work the three stages in order and do not look ahead.
#P Stage 1 - memorise this grid for 10 seconds, then cover it.
#C
.   X   .   .
.   .   .   X
X   .   .   .
.   .   X   .
#E
#P Stage 2 - spatial distractor. Are these two grids mirror images of each other across the vertical centre line?
#C
Left            Right
X   .   X       X   .   X
.   X   .       .   X   .
X   .   .       .   .   X
#E
#P Stage 3 - recall. In the Stage 1 grid, how many dots lay in the bottom two rows?

#Q 44|motionChallenge, discrete tick. A ball sits at row 1, column 1 of a 5 by 5 grid, moving diagonally down and to the right one cell per tick. It reflects off any wall it strikes, and on a corner both components reverse at once. Where is it after 6 ticks?
#O A) row 3, col 3     B) row 5, col 5     C) row 4, col 4     D) row 2, col 2

#SEC Section D - Coding Round (45 minutes, C / C++ / Java)

#SUB Problem 1 - Longest Subarray With Sum K
#P Given an integer array that may contain negatives and zeros, return the LENGTH of the longest contiguous subarray whose elements sum to exactly K. Return 0 if none exists. Use prefix sums with a hash map for O(n); the O(n squared) solution will time out.
#C
Input   arr = [10, 5, 2, 7, 1, 9], K = 15     Output   4    (5, 2, 7, 1)
Input   arr = [-1, 2, 3, -2, 4], K = 4        Output   5
#E

#SUB Problem 2 - Next Greater Element
#P For every element of an array, output the first element to its right that is strictly greater. Output -1 where none exists. O(n) using a monotonic stack.
#C
Input   [4, 5, 2, 25]        Output   [5, 25, 25, -1]
Input   [13, 7, 6, 12]       Output   [-1, 12, 12, -1]
#E
"""

SETH2 = r"""
#SET Test Set H2
#N Senior Analyst band - medium to hard.

#SEC Section A - Pseudo-code (Q1 to Q20)

#Q 1
#C
Integer a, b, c
Set a = 10, b = 4, c = 3
a = a - b * c / b + c
Print a
#E
#O A) 1     B) 4     C) 10     D) 13

#Q 2
#C
Integer f(Integer n, Integer d)
  if(n == 0)
    return 0
  End if
  return (n MOD d) + f(n / d, d)
End function f()
Print f(255, 4)
#E
#O A) 9     B) 3     C) 15     D) 12

#Q 3
#C
Integer i, j, c
Set c = 0, i = 1, j = 10
while(i < j)
  if((i + j) MOD 3 == 0)
    i = i + 2
  else
    j = j - 1
  End if
  c = c + 1
End while
Print i, j, c
#E
#O A) 5 6 6     B) 5 5 7     C) 3 5 7     D) 5 5 8

#Q 4
#C
Integer M[3][4], i, j, s
Set M = {{2,4,6,8},{1,3,5,7},{9,7,5,3}}
Set s = 0
for(each i from 0 to 2)
  for(each j from 0 to 3)
    if((i + j) MOD 2 == 0)
      s = s + M[i][j]
    else
      s = s - M[i][j]
    End if
  End for
End for
Print s
#E
#O A) -4     B) 0     C) 4     D) 12

#Q 5
#C
Integer swap(Integer p, Integer q)
  Integer t
  t = p
  p = q
  q = t
  return p + q
End function swap()
Integer x, y, r
Set x = 3, y = 8
r = swap(x, y)
Print x, y, r
#E
#O A) 8 3 11     B) 3 8 0     C) 8 3 5     D) 3 8 11

#Q 6
#C
String s
Integer i, c
Set s = "AABBBCC", c = 1
for(each i from 1 to LENGTH(s) - 1)
  if(s[i] != s[i-1])
    c = c + 1
  End if
End for
Print c
#E
#O A) 2     B) 3     C) 4     D) 7

#Q 7
#C
Integer A[6], i, mx, cur
Set A = {2, -3, 4, -1, 2, -5}
Set mx = A[0], cur = A[0]
for(each i from 1 to 5)
  if(cur + A[i] > A[i])
    cur = cur + A[i]
  else
    cur = A[i]
  End if
  if(cur > mx)
    mx = cur
  End if
End for
Print mx
#E
#O A) 2     B) 4     C) 5     D) 6

#Q 8
#C
Integer n, c, t
Set n = 6, c = 0
for(each t from 1 to n)
  if(n MOD t == 0)
    c = c + t
  End if
End for
if(c - n == n)
  Print "PERFECT"
else
  Print c - n
End if
#E
#O A) 6     B) 12     C) PERFECT     D) 0

#Q 9
#C
Integer f(Integer n)
  Integer c
  Set c = 0
  while(n != 1 AND c < 10)
    if(n MOD 2 == 0)
      n = n / 2
    else
      n = 3 * n + 1
    End if
    c = c + 1
  End while
  return c
End function f()
Print f(6)
#E
#O A) 7     B) 8     C) 9     D) 10

#Q 10
#C
Integer a, b
Set a = 29, b = 0
while(a > 0)
  b = b * 2 + (a MOD 2)
  a = a / 2
End while
Print b
#E
#O A) 15     B) 29     C) 31     D) 23

#Q 11
#C
Integer A[5], i, j, c
Set A = {1, 3, 2, 3, 1}
Set c = 0
for(each i from 0 to 4)
  for(each j from 0 to 4)
    if(A[i] == A[j] AND i < j)
      c = c + 1
    End if
  End for
End for
Print c
#E
#O A) 1     B) 2     C) 3     D) 4

#Q 12
#C
Integer x, y, z
Set x = 5
y = x AND (x - 1)
z = x OR (x + 1)
Print y, z
#E
#O A) 5 6     B) 1 7     C) 4 5     D) 4 7

#Q 13
#C
Integer A[4][4], i, j, s
Set A = {{1,2,3,4},{5,6,7,8},{9,1,2,3},{4,5,6,7}}
Set s = 0
for(each i from 0 to 3)
  for(each j from 0 to 3)
    if(i > j)
      s = s + A[i][j]
    End if
  End for
End for
Print s
#E
#O A) 16     B) 25     C) 30     D) 46

#Q 14
#C
Integer i, s
Set s = 0, i = 1
while(TRUE)
  s = s + i
  if(s > 15)
    break
  End if
  i = i + 2
End while
Print i, s
#E
#O A) 9 25     B) 7 9     C) 5 16     D) 7 16

#Q 15
#C
String s1, s2
Integer i, c
Set s1 = "ABCD", s2 = "CDAB", c = 0
for(each i from 0 to 3)
  if(s1[i] == s2[(i + 2) MOD 4])
    c = c + 1
  End if
End for
Print c
#E
#O A) 0     B) 2     C) 3     D) 4

#Q 16
#C
Integer f(Integer n)
  if(n < 10)
    return n
  End if
  return f(n / 10 + n MOD 10)
End function f()
Print f(789)
#E
#O A) 3     B) 6     C) 9     D) 24

#Q 17
#C
Integer A[7], lo, hi, mid, key
Set A = {1, 2, 4, 4, 4, 7, 9}
Set lo = 0, hi = 6, key = 4
while(lo < hi)
  mid = (lo + hi) / 2
  if(A[mid] < key)
    lo = mid + 1
  else
    hi = mid
  End if
End while
Print lo
#E
#O A) 2     B) 3     C) 4     D) 5

#Q 18
#C
Integer A[5], i, t, n
Set A = {4, 2, 7, 1, 9}
Set n = 5
for(each i from 0 to n / 2 - 1)
  t = A[i]
  A[i] = A[n - 1 - i]
  A[n - 1 - i] = t
End for
Print A[0], A[2], A[4]
#E
#O A) 4 7 9     B) 9 2 4     C) 9 7 4     D) 1 7 2

#Q 19
#C
Integer n, c, p
Set n = 12, c = 0, p = 1
while(p <= n)
  if((n AND p) != 0)
    c = c + 1
  End if
  p = p << 1
End while
Print c
#E
#O A) 1     B) 2     C) 3     D) 4

#Q 20
#C
Integer A[6], i, w
Set A = {0, 1, 0, 3, 0, 5}
Set w = 0
for(each i from 0 to 5)
  if(A[i] != 0)
    A[w] = A[i]
    w = w + 1
  End if
End for
while(w <= 5)
  A[w] = 0
  w = w + 1
End while
Print A[0], A[1], A[2], A[3]
#E
#O A) 0 1 0 3     B) 1 3 5 3     C) 5 3 1 0     D) 1 3 5 0

#SEC Section A - Computer Fundamentals (Q21 to Q30)

#Q 21|T(n) = 2T(n/2) + n resolves by the Master Theorem to:
#O A) O(n)     B) O(n log n)     C) O(n squared)     D) O(log n)

#Q 22|How many null keys does a Java HashMap permit?
#O A) 0     B) 1     C) Unlimited     D) Compile error

#Q 23|Which C++ idiom guarantees resource release on scope exit, including during exception unwinding?
#O A) goto cleanup     B) RAII via destructors
#O C) Static storage     D) Preprocessor macros

#Q 24|A relation is in BCNF when, for every non-trivial functional dependency X to Y:
#O A) Y is a candidate key     B) X is a superkey
#O C) X is a prime attribute     D) Y is prime

#Q 25|Which is true of a min-heap holding n elements?
#O A) The largest element is at the root
#O B) Searching an arbitrary key is O(log n)
#O C) Extract-min is O(log n)     D) It is a sorted array

#Q 26|TCP delivers reliability chiefly through:
#O A) Checksums alone     B) Routing tables
#O C) Sequence numbers plus acknowledgements with retransmission
#O D) Port multiplexing

#Q 27|Inserting already-sorted input into an unbalanced BST costs, in the worst case:
#O A) O(log n)     B) O(1)     C) O(n log n)     D) O(n) per insertion

#Q 28|For int *p = arr; the expression p + 3 advances the address by:
#O A) 3 bytes     B) 1 byte     C) 3 times sizeof(int) bytes     D) sizeof(p) bytes

#Q 29|Which index structure best serves range queries on an ordered column?
#O A) Hash index     B) B+ tree index     C) Bitmap index     D) Inverted index

#Q 30|Two threads increment a shared counter without synchronisation. The defect class is:
#O A) Deadlock     B) Starvation     C) Race condition     D) Livelock

#SEC Section B - English Communication (Q31 to Q38)

#Q 31|Not one of the proposed mitigations ____ the underlying race condition, though several ____ its symptoms.
#O A) address / masks     B) addresses / mask
#O C) address / mask     D) addresses / masks

#Q 32|Synonym of TENUOUS:
#O A) robust     B) flimsy     C) explicit     D) permanent

#Q 33|Antonym of PROLIFERATE:
#O A) multiply     B) dwindle     C) spread     D) escalate

#Q 34|"To paper over the cracks" means:
#O A) Conceal a problem rather than fix it     B) Document thoroughly
#O C) Reinforce a design     D) Finish a report

#Q 35|Find the error: "Neither the logs nor the metrics was conclusive, which left the team guessing."
#O A) Neither the logs     B) nor the metrics     C) was conclusive     D) No error

#Q 36|Which sentence contains no dangling modifier?
#O A) Having reviewed the schema, the migration was approved
#O B) Having reviewed the schema, the architect approved the migration
#O C) Having reviewed the schema, approval was given
#O D) Reviewing the schema, the migration seemed sound

#Q 37|Rearrange: (P) no amount of caching (Q) if the query itself is unindexed (R) will make (S) the endpoint responsive
#O A) QPRS     B) PRSQ     C) PQRS     D) QRPS

#Q 38|Read the passage and answer.
#C
Estimation error in software is not symmetric. Tasks that finish early save
the hours they save; tasks that overrun consume not only their own overrun
but the slack of everything scheduled behind them. A plan built on average
estimates is therefore optimistic even when the averages are correct.
#E
#P The argument turns on:
#O A) Estimates being systematically too low
#O B) Overruns propagating while early finishes do not
#O C) Averages being miscalculated     D) Developers padding estimates

#SEC Section C - Game-Based Cognitive (Q39 to Q44)

#Q 39|switchChallenge, single operator.
#C
Input     DIA   TRI   CIR   SQR
Output    SQR   CIR   DIA   TRI
#E
#O A) 3421     B) 4321     C) 4312     D) 2431

#Q 40|switchChallenge, two layers. Find Operator 2. Note that the output equals the input, so Operator 2 must be the inverse of Operator 1.
#C
Input         DIA   TRI   CIR   SQR
Operator 1    3142
Operator 2    ?
Output        DIA   TRI   CIR   SQR
#E
#O A) 4231     B) 2431     C) 3142     D) 2413

#Q 41|switchChallenge, three layers. Find the middle operator.
#C
Input         DIA   TRI   CIR   SQR
Operator 1    2143
Operator 2    ?
Operator 3    3412
Output        CIR   SQR   DIA   TRI
#E
#O A) 1234     B) 2143     C) 4321     D) 3142

#Q 42|digitChallenge. Digits 1 to 9, each used only once in the equation.
#C
_  *  _  +  _  /  _  =  31
#E
#O A) 4, 7, 6, 2     B) 5, 6, 2, 2     C) 3, 9, 8, 4     D) 6, 5, 2, 1

#Q 43|gridChallenge. Work the three stages in order.
#P Stage 1 - memorise this grid for 10 seconds, then cover it.
#C
.   .   X   .
X   .   .   .
.   .   .   X
.   X   .   .
#E
#P Stage 2 - distractor. Are these two grids mirror images across the vertical centre line?
#C
Left            Right
X   X   .       .   X   X
.   .   X       X   .   .
X   .   X       X   .   X
#E
#P Stage 3 - recall. In the Stage 1 grid, how many dots lay strictly above the main diagonal, that is with column index greater than row index?

#Q 44|motionChallenge, discrete tick. A ball starts at row 2, column 1 of a 4 by 4 grid, moving diagonally down and to the right, reflecting off walls. Position after 5 ticks?
#O A) row 1, col 2     B) row 2, col 3     C) row 3, col 4     D) row 4, col 3

#SEC Section D - Coding Round (45 minutes)

#SUB Problem 1 - Majority Element
#P An array of length n contains an element appearing strictly more than n/2 times. Return it. O(n) time and O(1) extra space; hash-map solutions violate the space constraint.
#C
Input   [2, 2, 1, 1, 1, 2, 2]     Output   2
Input   [3, 3, 4]                 Output   3
#E

#SUB Problem 2 - Merge Overlapping Intervals
#P Given a list of intervals as start and end pairs in arbitrary order, merge every overlapping or touching pair and return the merged set sorted by start.
#C
Input   [[1,3],[2,6],[8,10],[15,18]]     Output   [[1,6],[8,10],[15,18]]
Input   [[1,4],[4,5]]                    Output   [[1,5]]
#E
"""

SETH3 = r"""
#SET Test Set H3
#N Senior Analyst band - medium to hard.

#SEC Section A - Pseudo-code (Q1 to Q20)

#Q 1
#C
Integer a, b, c
Set a = 7, b = 2, c = 5
c = a MOD b + b MOD c * a
Print c
#E
#O A) 1     B) 3     C) 15     D) 8

#Q 2
#C
Integer f(Integer n)
  if(n <= 1)
    return 1
  End if
  if(n MOD 2 == 0)
    return f(n / 2)
  End if
  return f(n - 1) + 1
End function f()
Print f(20)
#E
#O A) 3     B) 2     C) 4     D) 1

#Q 3
#C
Integer i, j, s
Set s = 0
for(each i from 1 to 4)
  Set j = i
  while(j > 0)
    s = s + (i * j)
    j = j - 2
  End while
End for
Print s
#E
#O A) 30     B) 36     C) 45     D) 41

#Q 4
#C
Integer M[4][4], i, s
Set M = {{1,2,3,4},{5,6,7,8},{9,10,11,12},{13,14,15,16}}
Set s = 0
for(each i from 0 to 3)
  s = s + M[i][i] + M[i][3 - i]
End for
Print s
#E
#O A) 34     B) 68     C) 64     D) 72

#Q 5
#C
Integer a, b, c, t, i
Set a = 1, b = 2, c = 3
for(each i from 1 to 4)
  t = a
  a = b + c
  c = b
  b = t
End for
Print a, b, c
#E
#O A) 6 3 5     B) 8 3 6     C) 5 1 2     D) 8 6 3

#Q 6
#C
String s
Integer i, v, c
Set s = "SEQUENCE", v = 0, c = 0
for(each i from 0 to LENGTH(s) - 1)
  if(s[i] == 'A' OR s[i] == 'E' OR s[i] == 'I'
     OR s[i] == 'O' OR s[i] == 'U')
    v = v + 1
  else
    c = c + 1
  End if
End for
Print v - c
#E
#O A) 2     B) 0     C) -2     D) 4

#Q 7
#C
Integer A[6], i, j, c
Set A = {5, 1, 4, 2, 8, 3}
Set c = 0
for(each i from 0 to 5)
  for(each j from i + 1 to 5)
    if(A[i] > A[j])
      c = c + 1
    End if
  End for
End for
Print c
#E
#O A) 6     B) 8     C) 7     D) 9

#Q 8
#C
Integer n, s, d
Set n = 9875, s = 0
while(n > 0)
  d = n MOD 10
  n = n / 10
  if(d > 5)
    s = s * 10 + (d - 5)
  End if
End while
Print s
#E
#O A) 234     B) 432     C) 23     D) 2340

#Q 9
#C
Integer f(Integer n, Integer a)
  if(n == 0)
    return a
  End if
  return f(n - 1, a * n)
End function f()
Print f(5, 1) / f(3, 1)
#E
#O A) 24     B) 40     C) 6     D) 20

#Q 10
#C
Integer x, y
Set x = 22, y = 0
while(x != 0)
  y = y + (x AND 1)
  x = x >> 1
End while
Print y
#E
#O A) 4     B) 3     C) 2     D) 5

#Q 11
#C
Integer A[5], i, p
Set A = {1, 2, 3, 4, 5}
Set p = 1
for(each i from 0 to 4)
  if(A[i] MOD 2 == 1)
    p = p * A[i]
  else
    p = p + A[i]
  End if
End for
Print p
#E
#O A) 15     B) 120     C) 65     D) 45

#Q 12
#C
Integer i, j, c
Set c = 0, i = 0
while(i < 4)
  Set j = 0
  while(j < 4)
    if(i + j == 3 OR i == j)
      c = c + 1
    End if
    j = j + 1
  End while
  i = i + 1
End while
Print c
#E
#O A) 7     B) 6     C) 4     D) 8

#Q 13
#C
Integer A[7], i, k, t, tmp
Set A = {1, 2, 3, 4, 5, 6, 7}
Set k = 3
for(each i from 0 to 6)
  t = (i + k) MOD 7
  if(t > i)
    tmp = A[i]
    A[i] = A[t]
    A[t] = tmp
  End if
End for
Print A[0], A[3], A[6]
#E
#O A) 1 4 7     B) 4 7 1     C) 4 1 7     D) 5 2 3

#Q 14
#C
Integer n, r
Set n = 1, r = 0
repeat
  n = n * 2
  r = r + n
until(n >= 32)
Print n, r
#E
#O A) 32 30     B) 64 126     C) 32 62     D) 16 30

#Q 15
#C
String s
Integer i, j, f
Set s = "ABCBA"
Set i = 0, j = LENGTH(s) - 1, f = 1
while(i < j)
  if(s[i] != s[j])
    f = 0
    break
  End if
  i = i + 1
  j = j - 1
End while
Print f, i
#E
#O A) 1 0     B) 0 2     C) 1 5     D) 1 2

#Q 16
#C
Integer A[5], i, s, mx
Set A = {3, -2, 5, -1, 4}
Set s = 0, mx = 0
for(each i from 0 to 4)
  s = s + A[i]
  if(s < 0)
    s = 0
  End if
  if(s > mx)
    mx = s
  End if
End for
Print mx
#E
#O A) 6     B) 9     C) 12     D) 5

#Q 17
#C
Integer f(Integer a, Integer b)
  if(a < b)
    return 0
  End if
  return 1 + f(a - b, b)
End function f()
Print f(47, 6)
#E
#O A) 8     B) 6     C) 7     D) 5

#Q 18
#C
Integer A[4][3], i, j, mx, cs
Set A = {{3,8,1},{9,2,7},{4,6,5},{2,9,3}}
Set mx = 0
for(each j from 0 to 2)
  Set cs = 0
  for(each i from 0 to 3)
    cs = cs + A[i][j]
  End for
  if(cs > mx)
    mx = cs
  End if
End for
Print mx
#E
#O A) 18     B) 16     C) 59     D) 25

#Q 19
#C
Integer n, c, i
Set n = 36, c = 0
for(each i from 1 to n)
  if(i * i <= n AND n MOD i == 0)
    c = c + 2
    if(i * i == n)
      c = c - 1
    End if
  End if
End for
Print c
#E
#O A) 10     B) 9     C) 8     D) 6

#Q 20
#C
Integer A[6], i, j, t, n
Set A = {6, 5, 4, 3, 2, 1}
Set n = 6
for(each i from 1 to n - 1)
  t = A[i]
  Set j = i - 1
  while(j >= 0 AND A[j] > t)
    A[j + 1] = A[j]
    j = j - 1
  End while
  A[j + 1] = t
End for
Print A[0], A[5]
#E
#O A) 6 1     B) 1 5     C) 2 6     D) 1 6

#SEC Section A - Computer Fundamentals (Q21 to Q30)

#Q 21|Appending to a dynamic array that doubles its capacity when full costs:
#O A) O(n) per append     B) O(1) amortised     C) O(log n)     D) O(n log n)

#Q 22|Which statement about Java's finally block is FALSE?
#O A) It runs after try or catch completes     B) It runs even if catch throws
#O C) It runs even after System.exit(0)     D) It can override a return value

#Q 23|Per the C standard, sizeof(char) is:
#O A) Always 1     B) Platform-dependent     C) 2     D) 4

#Q 24|R(A,B,C) with A as primary key and functional dependencies A to B and B to C is in:
#O A) 1NF only     B) 2NF but not 3NF     C) 3NF     D) BCNF

#Q 25|Building a heap from an unsorted array using bottom-up heapify costs:
#O A) O(n log n)     B) O(n)     C) O(log n)     D) O(n squared)

#Q 26|A page fault is classified as major when:
#O A) The page is resident but marked invalid
#O B) The page must be fetched from disk
#O C) The TLB missed     D) The frame is dirty

#Q 27|A depth-first search on a directed graph reports a cycle upon encountering:
#O A) Any visited node     B) A node currently on the recursion stack
#O C) A leaf     D) A disconnected component

#Q 28|The static keyword on a file-scope C function means:
#O A) It cannot be called
#O B) Internal linkage, visible only in that translation unit
#O C) It is thread-safe     D) Its locals persist

#Q 29|Which discipline prevents deadlock among threads acquiring multiple mutexes?
#O A) Randomised ordering     B) A single consistent global acquisition order
#O C) Longer timeouts     D) More mutexes

#Q 30|Which pair, taken together, uniquely reconstructs a binary tree?
#O A) Preorder plus postorder     B) Inorder plus preorder
#O C) Level order alone     D) Inorder alone

#SEC Section B - English Communication (Q31 to Q38)

#Q 31|The findings, ____ compelling, ____ replication before the team commits to a rewrite.
#O A) while / require     B) while / requires
#O C) whilst / requiring     D) although / requires

#Q 32|Synonym of EQUIVOCAL:
#O A) unambiguous     B) ambiguous     C) forceful     D) verified

#Q 33|Antonym of SALIENT:
#O A) prominent     B) inconspicuous     C) striking     D) notable

#Q 34|"To move the goalposts" means:
#O A) Change the criteria after work has begun     B) Relocate a resource
#O C) Increase the budget     D) Reassign ownership

#Q 35|Find the error: "The data suggests that latency spikes correlates with cache evictions."
#O A) The data suggests     B) that latency spikes     C) correlates with     D) No error

#Q 36|Which uses the subjunctive correctly?
#O A) If the index was present, the query would be fast
#O B) If the index were present, the query would be fast
#O C) If the index is present, the query would be fast
#O D) If the index were present, the query will be fast

#Q 37|Rearrange: (P) that the fix is safe (Q) a passing test suite (R) is not evidence (S) only that the tested paths behave
#O A) QRPS     B) PQRS     C) QPRS     D) RQPS

#Q 38|Read the passage and answer.
#C
The observability argument is often framed as logs versus metrics versus
traces, as though a team must choose. In practice the three answer different
questions: metrics tell you that something changed, traces tell you where,
and logs tell you what. A team that invests in only one will find itself able
to detect an incident it cannot explain, or explain one it detected too late.
#E
#P The passage concludes the three are:
#O A) Interchangeable     B) Complementary rather than competing
#O C) Equally expensive     D) Redundant at scale

#SEC Section C - Game-Based Cognitive (Q39 to Q44)

#Q 39|switchChallenge, single operator.
#C
Input     SQR   STR   DIA   CIR
Output    DIA   CIR   SQR   STR
#E
#O A) 4312     B) 3421     C) 3412     D) 1342

#Q 40|switchChallenge, two layers. Find Operator 2.
#C
Input         SQR   STR   DIA   CIR
Operator 1    4231
Operator 2    ?
Output        STR   DIA   SQR   CIR
#E
#O A) 3412     B) 2341     C) 4123     D) 1432

#Q 41|switchChallenge, three layers. Find the middle operator.
#C
Input         SQR   STR   DIA   CIR
Operator 1    1324
Operator 2    ?
Operator 3    2413
Output        SQR   STR   CIR   DIA
#E
#O A) 2314     B) 3241     C) 1432     D) 4123

#Q 42|digitChallenge. Digits 1 to 9, each used only once in the equation.
#C
_  /  _  +  _  *  _  =  29
#E
#O A) 9, 3, 8, 2     B) 6, 3, 9, 3     C) 8, 4, 9, 3     D) 8, 2, 5, 6

#Q 43|gridChallenge. Work the three stages in order.
#P Stage 1 - memorise this grid for 10 seconds, then cover it.
#C
X   .   .   .
.   .   X   .
.   X   .   .
.   .   .   X
#E
#P Stage 2 - distractor. Grid A rotated 180 degrees produces which option?
#C
Grid A            Option A          Option B
X   X   .         .   .   .         .   X   X
.   .   X         X   .   .         X   .   .
.   .   .         .   X   X         .   .   .

                  Option C          Option D
                  .   .   .         X   X   .
                  .   .   X         X   .   .
                  X   X   .         .   .   .
#E
#O A) Option A     B) Option B     C) Option C     D) Option D
#P Stage 3 - recall. In the Stage 1 grid, which row held a dot in column 2?

#Q 44|motionChallenge, discrete tick. A ball at row 3, column 1 of a 5 by 5 grid moves diagonally up and to the right, reflecting off walls. Position after 6 ticks?
#O A) row 4, col 4     B) row 5, col 3     C) row 1, col 3     D) row 3, col 5

#SEC Section D - Coding Round (45 minutes)

#SUB Problem 1 - Longest Consecutive Sequence
#P Given an unsorted integer array, return the length of the longest run of consecutive integers present. Order in the array is irrelevant. O(n) expected; sorting is O(n log n) and loses marks.
#C
Input   [100, 4, 200, 1, 3, 2]           Output   4    (1, 2, 3, 4)
Input   [9, 1, 4, 7, 3, 2, 6, 8, 5]      Output   9
#E

#SUB Problem 2 - Kth Largest Element
#P Given an unsorted array and k, return the k-th largest element WITHOUT fully sorting the array. Target O(n log k) with a min-heap of size k, or average O(n) with quickselect.
#C
Input   [3, 2, 1, 5, 6, 4], k = 2                 Output   5
Input   [3, 2, 3, 1, 2, 4, 5, 5, 6], k = 4        Output   4
#E
"""

SETH4 = r"""
#SET Test Set H4
#N Senior Analyst band - medium to hard.

#SEC Section A - Pseudo-code (Q1 to Q20)

#Q 1
#C
Integer a, b, c
Set a = 9, b = 5, c = 2
b = a / c * c
c = a - b
Print b, c
#E
#O A) 9 0     B) 8 1     C) 10 -1     D) 8 4

#Q 2
#C
Integer f(Integer n)
  if(n == 1)
    return 0
  End if
  return 1 + f(n / 2)
End function f()
Print f(100)
#E
#O A) 5     B) 7     C) 6     D) 8

#Q 3
#C
Integer i, j, s
Set s = 0, i = 2
while(i <= 8)
  Set j = i
  while(j <= 8)
    s = s + 1
    j = j + i
  End while
  i = i + 2
End while
Print s
#E
#O A) 7     B) 8     C) 9     D) 10

#Q 4
#C
Integer M[3][3], i, j, c
Set M = {{1,0,1},{0,1,0},{1,1,0}}
Set c = 0
for(each i from 0 to 2)
  for(each j from 0 to 2)
    if(M[i][j] == 1 AND M[j][i] == 1)
      c = c + 1
    End if
  End for
End for
Print c
#E
#O A) 3     B) 5     C) 4     D) 6

#Q 5
#C
Integer a, b, c, i
Set a = 2, b = 1, c = 0
for(each i from 1 to 5)
  c = a * b - c
  a = b
  b = c
End for
Print a, b, c
#E
#O A) 0 0 0     B) 2 1 0     C) 1 2 2     D) 2 0 0

#Q 6
#C
String s
Integer i, c
Set s = "PARALLEL", c = 0
for(each i from 0 to LENGTH(s) - 1)
  if(s[i] == 'L' OR s[i] == 'A')
    c = c + 1
  End if
End for
Print c
#E
#O A) 4     B) 5     C) 6     D) 3

#Q 7
#C
Integer A[6], i, j, t
Set A = {1, 5, 3, 2, 4, 6}
for(each i from 0 to 5)
  for(each j from 0 to 4)
    if(A[j] > A[j+1])
      t = A[j]
      A[j] = A[j+1]
      A[j+1] = t
    End if
  End for
End for
Print A[1], A[4]
#E
#O A) 5 4     B) 2 5     C) 1 6     D) 3 4

#Q 8
#C
Integer n, s, d, c
Set n = 4823, s = 0, c = 0
while(n > 0)
  d = n MOD 10
  n = n / 10
  c = c + 1
  if(c MOD 2 == 1)
    s = s + d
  else
    s = s - d
  End if
End while
Print s
#E
#O A) 3     B) 5     C) 9     D) 17

#Q 9
#C
Integer f(Integer n)
  if(n <= 0)
    return 1
  End if
  return f(n - 1) * 2 - 1
End function f()
Print f(4)
#E
#O A) 16     B) 15     C) 1     D) 7

#Q 10
#C
Integer a, b, c
Set a = 6, b = 10
c = a XOR b
a = a AND b
b = a OR c
Print a, b, c
#E
#O A) 2 14 12     B) 6 10 12     C) 2 12 14     D) 14 2 12

#Q 11
#C
Integer A[5], i, s
Set A = {2, 4, 6, 8, 10}
Set s = 0
for(each i from 0 to 4)
  if(i > 0 AND A[i] > A[i-1])
    s = s + A[i] - A[i-1]
  End if
End for
Print s
#E
#O A) 30     B) 8     C) 10     D) 2

#Q 12
#C
Integer i, j, c
Set c = 0
for(each i from 1 to 5)
  Set j = 1
  while(j <= i)
    if((i + j) MOD 2 == 0)
      c = c + 1
    End if
    j = j + 1
  End while
End for
Print c
#E
#O A) 8     B) 9     C) 10     D) 15

#Q 13
#C
Integer A[7], i, lo, hi, mid, key
Set A = {2, 4, 6, 8, 10, 12, 14}
Set lo = 0, hi = 6, key = 9, i = 0
while(lo <= hi)
  mid = (lo + hi) / 2
  i = i + 1
  if(A[mid] == key)
    break
  End if
  if(A[mid] < key)
    lo = mid + 1
  else
    hi = mid - 1
  End if
End while
Print i, lo
#E
#O A) 3 4     B) 4 4     C) 3 5     D) 2 4

#Q 14
#C
Integer n, r, c
Set n = 5, r = 1, c = 0
while(c < 4)
  r = r * n - c
  c = c + 1
End while
Print r
#E
#O A) 625     B) 587     C) 590     D) 118

#Q 15
#C
String s
Integer i, mx, cur
Set s = "AABBBBCC"
Set mx = 1, cur = 1
for(each i from 1 to LENGTH(s) - 1)
  if(s[i] == s[i-1])
    cur = cur + 1
  else
    cur = 1
  End if
  if(cur > mx)
    mx = cur
  End if
End for
Print mx
#E
#O A) 2     B) 3     C) 4     D) 8

#Q 16
#C
Integer A[5], i, j, c, f
Set A = {3, 1, 4, 1, 5}
Set c = 0
for(each i from 0 to 4)
  Set j = 0, f = 0
  while(j < i)
    if(A[j] == A[i])
      f = 1
    End if
    j = j + 1
  End while
  if(f == 0)
    c = c + 1
  End if
End for
Print c
#E
#O A) 5     B) 3     C) 4     D) 2

#Q 17
#C
Integer f(Integer n)
  if(n < 3)
    return n
  End if
  return f(n - 1) - f(n - 2) + f(n - 3)
End function f()
Print f(6)
#E
#O A) 1     B) 0     C) 2     D) 3

#Q 18
#C
Integer M[4][4], i, j, t
Set M = {{1,2,3,4},{5,6,7,8},{9,10,11,12},{13,14,15,16}}
for(each i from 0 to 1)
  for(each j from 0 to 3)
    t = M[i][j]
    M[i][j] = M[3 - i][j]
    M[3 - i][j] = t
  End for
End for
Print M[0][0], M[1][1], M[3][3]
#E
#O A) 13 10 4     B) 1 6 16     C) 13 6 4     D) 4 10 13

#Q 19
#C
Integer n, m, g, l, t
Set n = 12, m = 18
Set g = n, l = m
while(l != 0)
  t = l
  l = g MOD l
  g = t
End while
Print g, (n * m) / g
#E
#O A) 6 36     B) 6 216     C) 2 108     D) 18 12

#Q 20
#C
Integer A[8], lo, hi, mid
Set A = {5, 6, 7, 1, 2, 3, 4, 5}
Set lo = 0, hi = 7
while(lo < hi)
  mid = (lo + hi) / 2
  if(A[mid] > A[hi])
    lo = mid + 1
  else
    hi = mid
  End if
End while
Print lo, A[lo]
#E
#O A) 3 1     B) 0 5     C) 4 2     D) 3 7

#SEC Section A - Computer Fundamentals (Q21 to Q30)

#Q 21|Which sort performs best on a nearly sorted array?
#O A) QuickSort with first-element pivot     B) Insertion sort
#O C) Heap sort     D) Selection sort

#Q 22|In Java, the == operator applied to two Integer objects each holding 1000 compares:
#O A) Values     B) References     C) Hash codes     D) It is always true

#Q 23|Which C++ smart pointer provides shared ownership via reference counting?
#O A) unique_ptr     B) shared_ptr     C) weak_ptr     D) auto_ptr

#Q 24|A composite index on (A, B) efficiently serves a query filtering only on:
#O A) B alone     B) A alone     C) Neither     D) Both individually

#Q 25|Worst-case auxiliary space of DFS on a graph with V vertices:
#O A) O(1)     B) O(V)     C) O(V squared)     D) O(log V)

#Q 26|With all burst times known in advance, which scheduler minimises average waiting time?
#O A) FCFS     B) Round Robin     C) Shortest Job First     D) Priority

#Q 27|An IPv4 /26 subnet provides how many usable host addresses?
#O A) 64     B) 62     C) 30     D) 126

#Q 28|Given only a pointer to a node, which operation is O(1) on a doubly linked list but O(n) on a singly linked list?
#O A) Insert after it     B) Traverse     C) Delete that node     D) Search

#Q 29|In C, char *s = "abc"; followed by s[0] = 'x'; is:
#O A) Valid     B) Undefined behaviour - string literals are not writable
#O C) Always a compile error     D) Valid but slow

#Q 30|Which protocol guarantees serialisable schedules?
#O A) Timestamp ordering alone     B) Two-phase locking
#O C) Read Committed     D) Optimistic reads

#SEC Section B - English Communication (Q31 to Q38)

#Q 31|Each of the microservices, along with its sidecar proxy, ____ independently deployable.
#O A) are     B) is     C) have been     D) were

#Q 32|Synonym of SPURIOUS:
#O A) genuine     B) counterfeit     C) urgent     D) abundant

#Q 33|Antonym of EXACERBATE:
#O A) aggravate     B) alleviate     C) intensify     D) provoke

#Q 34|"To bikeshed" means:
#O A) Argue over trivia while ignoring the substantive issue
#O B) Build a prototype     C) Store unused code     D) Delay indefinitely

#Q 35|Find the error: "Between you and I, the estimate was never realistic."
#O A) Between you and I     B) the estimate     C) was never realistic     D) No error

#Q 36|Which sentence uses "comprise" correctly?
#O A) The system is comprised of four services
#O B) The system comprises four services
#O C) The system comprises of four services
#O D) Four services comprise into the system

#Q 37|Rearrange: (P) the bug was reproducible (Q) it took three weeks (R) but only under load (S) to construct a load harness
#O A) PRQS     B) QSPR     C) PQRS     D) RPQS

#Q 38|Read the passage and answer.
#C
Refactoring is often justified by future velocity, a benefit that is real but
unfalsifiable in any single case. The team that refactors and then ships
faster cannot prove the refactor caused it; the team that skips it and slows
down cannot prove the omission was the reason. The argument for refactoring
therefore rests on accumulated experience rather than local measurement.
#E
#P The justification for refactoring is characterised as:
#O A) Unfounded
#O B) Supported inductively rather than demonstrable case by case
#O C) Purely aesthetic     D) Measurable with better tooling

#SEC Section C - Game-Based Cognitive (Q39 to Q44)

#Q 39|switchChallenge, single operator.
#C
Input     TRI   SQR   CIR   STR
Output    STR   CIR   TRI   SQR
#E
#O A) 3421     B) 4321     C) 2413     D) 4312

#Q 40|switchChallenge, two layers, with the FIRST operator missing. Operator 2 is given; deduce Operator 1 by first inverting Operator 2 to recover the hidden intermediate row.
#C
Input         TRI   SQR   CIR   STR
Operator 1    ?
Operator 2    2143
Output        STR   CIR   TRI   SQR
#E
#O A) 4312     B) 3421     C) 2341     D) 1432

#Q 41|switchChallenge, three layers. Find the middle operator.
#C
Input         TRI   SQR   CIR   STR
Operator 1    2314
Operator 2    ?
Operator 3    4123
Output        CIR   TRI   SQR   STR
#E
#O A) 4213     B) 2431     C) 3142     D) 1324

#Q 42|digitChallenge. Digits 1 to 9, each used only once in the equation.
#C
_  *  _  +  _  -  _  =  30
#E
#O A) 6, 5, 3, 3     B) 8, 3, 9, 2     C) 7, 4, 5, 3     D) 9, 2, 7, 1

#Q 43|gridChallenge. Work the three stages in order.
#P Stage 1 - memorise this grid for 10 seconds, then cover it.
#C
.   .   .   X
X   .   .   .
.   X   X   .
.   .   .   .
#E
#P Stage 2 - distractor. Is this grid symmetric about the main diagonal, running from top-left to bottom-right?
#C
X   .   X
.   X   .
X   .   X
#E
#P Stage 3 - recall. How many dots were in row 3 of the Stage 1 grid?

#Q 44|motionChallenge, discrete tick. A ball at row 1, column 4 of a 4 by 4 grid moves diagonally down and to the left, reflecting off walls. Position after 5 ticks?
#O A) row 4, col 1     B) row 3, col 2     C) row 2, col 3     D) row 1, col 4

#SEC Section D - Coding Round (45 minutes)

#SUB Problem 1 - Product of Array Except Self
#P For each index i, output the product of every element except the one at i. Division is NOT allowed. O(n) time; the output array does not count toward extra space.
#C
Input   [1, 2, 3, 4]              Output   [24, 12, 8, 6]
Input   [-1, 1, 0, -3, 3]         Output   [0, 0, 9, 0, 0]
#E

#SUB Problem 2 - Set Matrix Zeroes
#P Given an m by n matrix, if any element is 0, set that element's entire row and column to 0. Do it in place with O(1) extra space. Zeroing as you scan is wrong because it cascades.
#C
Input        Output
1 1 1        1 0 1
1 0 1        0 0 0
1 1 1        1 0 1
#E
"""

SETH5 = r"""
#SET Test Set H5
#N Senior Analyst band - medium to hard.

#SEC Section A - Pseudo-code (Q1 to Q20)

#Q 1
#C
Integer a, b, c
Set a = 17, b = 6, c = 4
c = a MOD b MOD c
b = a / b / c
Print b, c
#E
#O A) 2 1     B) 1 2     C) 2 5     D) 4 1

#Q 2
#C
Integer f(Integer n)
  if(n == 0)
    return 0
  End if
  if(n MOD 3 == 0)
    return f(n - 1) + 3
  End if
  return f(n - 1) + 1
End function f()
Print f(9)
#E
#O A) 9     B) 12     C) 15     D) 18

#Q 3
#C
Integer i, j, c
Set c = 0, i = 1
while(i <= 16)
  Set j = i
  while(j <= 16)
    c = c + 1
    j = j * 2
  End while
  i = i * 4
End while
Print c
#E
#O A) 8     B) 9     C) 10     D) 12

#Q 4
#C
Integer M[3][3], i, j, s, mn
Set M = {{4,1,7},{2,8,3},{6,5,9}}
Set s = 0
for(each i from 0 to 2)
  Set mn = M[i][0]
  for(each j from 1 to 2)
    if(M[i][j] < mn)
      mn = M[i][j]
    End if
  End for
  s = s + mn
End for
Print s
#E
#O A) 8     B) 12     C) 6     D) 24

#Q 5
#C
Integer p, q, r, i
Set p = 1, q = 0, r = 0
for(each i from 1 to 5)
  r = p + q
  q = p
  p = r
End for
Print p, q, r
#E
#O A) 8 5 8     B) 5 3 5     C) 8 5 13     D) 13 8 13

#Q 6
#C
String s
Integer i, c
Set s = "ABABABA", c = 0
for(each i from 0 to LENGTH(s) - 3)
  if(s[i] == s[i+2])
    c = c + 1
  End if
End for
Print c
#E
#O A) 3     B) 4     C) 5     D) 7

#Q 7
#C
Integer A[6], i, e, o
Set A = {7, 2, 9, 4, 1, 6}
Set e = 0, o = 0
for(each i from 0 to 5)
  if(A[i] MOD 2 == 0)
    e = e + A[i]
  else
    o = o * 10 + A[i]
  End if
End for
Print e, o
#E
#O A) 12 791     B) 12 17     C) 6 791     D) 12 197

#Q 8
#C
Integer n, c
Set n = 1, c = 0
while(c < 5)
  n = n * 3 + c
  c = c + 1
End while
Print n
#E
#O A) 243     B) 301     C) 297     D) 99

#Q 9
#C
Integer f(Integer n, Integer k)
  if(k == 0 OR k == n)
    return 1
  End if
  return f(n - 1, k - 1) + f(n - 1, k)
End function f()
Print f(5, 2)
#E
#O A) 5     B) 10     C) 20     D) 15

#Q 10
#C
Integer a, b
Set a = 20, b = 12
Print (a AND b), (a OR b), (a XOR b)
#E
#O A) 4 28 24     B) 12 20 8     C) 4 24 28     D) 8 28 20

#Q 11
#C
Integer A[5], i, j
Set A = {10, 20, 30, 40, 50}
Set i = 0
while(i < 5)
  Set j = i + 1
  while(j < 5)
    if(A[i] + A[j] == 60)
      Print i, j
    End if
    j = j + 1
  End while
  i = i + 1
End while
#E
#O A) 0 4 only     B) 0 4 and 1 3     C) 1 3 only     D) No output

#Q 12
#C
Integer n, s, t
Set n = 7, s = 0
Set t = n
while(t > 0)
  s = s + t * t
  t = t - 2
End while
Print s
#E
#O A) 84     B) 140     C) 49     D) 91

#Q 13
#C
String s1, s2
Integer i, c1, c2
Set s1 = "SILENT", s2 = "LISTEN"
Set c1 = 0, c2 = 0
for(each i from 0 to 5)
  c1 = c1 + (s1[i] - 'A')
  c2 = c2 + (s2[i] - 'A')
End for
if(c1 == c2)
  Print "MATCH"
else
  Print c1 - c2
End if
#E
#O A) MATCH     B) 0     C) 6     D) -6

#Q 14
#C
Integer A[6], i, k, c
Set A = {1, 2, 3, 4, 5, 6}
Set k = 2, c = 0
for(each i from 0 to 5)
  if(A[i] MOD k == 0)
    c = c + A[i]
    k = k + 1
  End if
End for
Print c, k
#E
#O A) 20 7     B) 12 4     C) 21 7     D) 20 6

#Q 15
#C
Integer M[3][3], i, j, s1, s2
Set M = {{2,7,6},{9,5,1},{4,3,8}}
Set s2 = 0
for(each i from 0 to 2)
  Set s1 = 0
  for(each j from 0 to 2)
    s1 = s1 + M[i][j]
  End for
  if(s1 != 15)
    s2 = s2 + 1
  End if
End for
Print s2
#E
#O A) 0     B) 1     C) 3     D) 15

#Q 16
#C
Integer f(Integer n)
  if(n <= 1)
    return n
  End if
  Integer a, b, c, i
  Set a = 0, b = 1
  for(each i from 2 to n)
    c = a + b
    a = b
    b = c
  End for
  return b
End function f()
Print f(8)
#E
#O A) 13     B) 21     C) 34     D) 8

#Q 17
#C
Integer A[7], i, w
Set A = {1, 1, 2, 2, 2, 3, 3}
Set w = 0
for(each i from 0 to 6)
  if(i == 0 OR A[i] != A[i-1])
    A[w] = A[i]
    w = w + 1
  End if
End for
Print w, A[0], A[1], A[2]
#E
#O A) 3 1 2 3     B) 7 1 1 2     C) 3 1 2 2     D) 4 1 2 3

#Q 18
#C
Integer n, r, t
Set n = 1234, r = 0
Set t = n
while(t > 0)
  r = r * 10 + (t MOD 10)
  t = t / 10
End while
if(r == n)
  Print "PALINDROME"
else
  Print r - n
End if
#E
#O A) PALINDROME     B) 3087     C) 4321     D) 1234

#Q 19
#C
Integer A[8], lo, hi, mid, key, r
Set A = {1, 3, 5, 7, 9, 11, 13, 15}
Set lo = 0, hi = 7, key = 11, r = 0
while(lo <= hi)
  mid = lo + (hi - lo) / 2
  r = r + 1
  if(A[mid] == key)
    break
  End if
  if(A[mid] < key)
    lo = mid + 1
  else
    hi = mid - 1
  End if
End while
Print r, mid
#E
#O A) 2 5     B) 3 5     C) 2 4     D) 1 3

#Q 20
#C
Integer A[5], B[5], i, j
Set A = {1, 2, 3, 4, 5}
Set j = 0
for(each i from 4 down to 0)
  if(A[i] MOD 2 == 1)
    B[j] = A[i]
    j = j + 1
  End if
End for
for(each i from 4 down to 0)
  if(A[i] MOD 2 == 0)
    B[j] = A[i]
    j = j + 1
  End if
End for
Print B[0], B[2], B[4]
#E
#O A) 5 1 2     B) 1 3 5     C) 5 3 1     D) 1 5 2

#SEC Section A - Computer Fundamentals (Q21 to Q30)

#Q 21|Lower bound on comparisons for any comparison-based sort of n elements:
#O A) Omega(n)     B) Omega(n log n)     C) Omega(log n)     D) Omega(n squared)

#Q 22|An unchecked exception propagating out of Java's main results in:
#O A) A compile error
#O B) The JVM printing the stack trace and terminating the thread
#O C) Silent suppression     D) main restarting

#Q 23|In C++, const placed after a member function's parameter list means:
#O A) The return value is const
#O B) The function cannot modify non-mutable members
#O C) The function is static     D) Parameters are const

#Q 24|Which anomaly occurs under Read Committed but not Repeatable Read?
#O A) Dirty read     B) Non-repeatable read     C) Phantom read     D) Lost update

#Q 25|Extracting the root from a min-heap and restoring the heap property costs:
#O A) O(1)     B) O(log n)     C) O(n)     D) O(n log n)

#Q 26|Copy-on-write in fork() means:
#O A) Pages are duplicated immediately
#O B) Pages stay shared until one process writes
#O C) The child cannot write     D) Memory is swapped to disk

#Q 27|Which IPv4 header field stops packets circulating indefinitely?
#O A) Checksum     B) TTL     C) Flags     D) Protocol

#Q 28|Topological sort is defined for:
#O A) Any graph     B) Directed acyclic graphs
#O C) Undirected trees     D) Complete graphs

#Q 29|For int a[5]; the expression sizeof(a) / sizeof(a[0]) evaluates to:
#O A) 5     B) 20     C) 4     D) 1

#Q 30|Which normal form's decomposition is not always dependency-preserving?
#O A) 1NF     B) 2NF     C) 3NF     D) BCNF

#SEC Section B - English Communication (Q31 to Q38)

#Q 31|The set of assumptions on which the design rests ____ never been documented, which ____ why reviewers disagree.
#O A) have / explain     B) has / explains
#O C) have / explains     D) has / explain

#Q 32|Synonym of INCHOATE:
#O A) complete     B) rudimentary     C) refined     D) urgent

#Q 33|Antonym of CIRCUMSPECT:
#O A) cautious     B) reckless     C) prudent     D) wary

#Q 34|"To gold-plate" a feature means:
#O A) Add refinement beyond what was requested     B) Make it expensive
#O C) Document it heavily     D) Deprecate it

#Q 35|Find the error: "Neither of the two candidates were able to explain their own design."
#O A) Neither of     B) the two candidates     C) were able     D) No error

#Q 36|Which sentence is free of a misplaced modifier?
#O A) We only deployed the fix to staging, not production
#O B) We deployed the fix only to staging, not production
#O C) Only we deployed the fix to staging, not production
#O D) We deployed only the fix to staging, not production

#Q 37|Rearrange: (P) the incident review concluded (Q) not the deploy that exposed it (R) that the root cause (S) was the missing constraint
#O A) PRSQ     B) PQRS     C) RSPQ     D) PRQS

#Q 38|Read the passage and answer.
#C
A postmortem that names an individual has already failed. The question is not
who typed the command but why the system permitted a single command to cause
that much damage. Blame terminates inquiry at the most convenient point, which
is almost never the most informative one.
#E
#P The author objects to naming individuals chiefly because it:
#O A) Is unkind     B) Halts investigation before the systemic cause surfaces
#O C) Carries legal risk     D) Degrades documentation

#SEC Section C - Game-Based Cognitive (Q39 to Q44)

#Q 39|switchChallenge, single operator.
#C
Input     CIR   STR   SQR   TRI
Output    SQR   TRI   CIR   STR
#E
#O A) 4312     B) 3142     C) 3412     D) 2341

#Q 40|switchChallenge, two layers. Find Operator 2.
#C
Input         CIR   STR   SQR   TRI
Operator 1    4213
Operator 2    ?
Output        CIR   TRI   SQR   STR
#E
#O A) 2413     B) 3142     C) 4321     D) 1324

#Q 41|switchChallenge, three layers. Find the middle operator. The output equals the input, so the three operators compose to the identity.
#C
Input         CIR   STR   SQR   TRI
Operator 1    4321
Operator 2    ?
Operator 3    3412
Output        CIR   STR   SQR   TRI
#E
#O A) 4132     B) 2143     C) 1324     D) 3412

#Q 42|digitChallenge. Digits 1 to 9, each used only once in the equation.
#C
_  /  _  *  _  -  _  =  19
#E
#O A) 8, 2, 6, 5     B) 6, 2, 7, 2     C) 9, 3, 8, 4     D) 6, 3, 9, 2

#Q 43|gridChallenge. Work the three stages in order.
#P Stage 1 - memorise this grid for 12 seconds, then cover it.
#C
X   .   .   X
.   .   X   .
.   X   .   .
X   .   .   .
#E
#P Stage 2 - distractor. Grid A rotated 90 degrees clockwise produces which option?
#C
Grid A            Option A          Option B
X   .   .         .   X   X         X   X   .
X   X   .         .   X   .         .   X   .
.   .   X         X   .   .         .   .   X

                  Option C          Option D
                  X   .   .         .   .   X
                  .   X   X         .   X   .
                  .   .   X         X   X   .
#E
#O A) Option A     B) Option B     C) Option C     D) Option D
#P Stage 3 - recall. How many dots were in column 1 of the Stage 1 grid?

#Q 44|motionChallenge, discrete tick. A ball at row 3, column 3 of a 5 by 5 grid moves diagonally up and to the left, reflecting off walls. Position after 7 ticks?
#O A) row 5, col 5     B) row 4, col 4     C) row 3, col 3     D) row 1, col 1

#SEC Section D - Coding Round (45 minutes)

#SUB Problem 1 - Search in Rotated Sorted Array
#P A sorted array of distinct integers has been rotated an unknown number of times. Given a target, return its index or -1. Must run in O(log n); a linear scan fails the constraint.
#C
Input   [4, 5, 6, 7, 0, 1, 2], target = 0     Output   4
Input   [4, 5, 6, 7, 0, 1, 2], target = 3     Output   -1
#E

#SUB Problem 2 - Decode Ways
#P A message of digits was encoded with A equal to 1 through Z equal to 26. Return the number of distinct ways to decode it. Leading zeros make a grouping invalid, so "06" cannot be read as 6. Dynamic programming, O(n) time.
#C
Input   "12"      Output   2     (AB, L)
Input   "226"     Output   3     (BZ, VF, BBF)
Input   "06"      Output   0
#E
"""

KEYS = r"""
#PART Answer Keys
#P Section A runs Q1 to Q30, Section B runs Q31 to Q40 in Sets 1 to 5 and Q31 to Q38 in Sets H1 to H5, and Section C occupies the remaining numbers. Section D is open-ended and is graded on test cases passed and time complexity, so no key is given.
#N Every pseudo-code answer in this book was traced from first principles rather than copied from a published key.

#SEC Set 1
#K Section A   1-B   2-C   3-A   4-B   5-B   6-A   7-A   8-B   9-B   10-B
#K             11-A  12-B  13-A  14-B  15-A  16-B  17-A  18-B  19-B  20-B
#K             21-B  22-C  23-C  24-B  25-B  26-C  27-C  28-B  29-C  30-B
#K Section B   31-C  32-B  33-C  34-B  35-B  36-A  37-A  38-A  39-B  40-C
#K Section C   41-A (CIR)      42-B  5 * 3 - 2 = 13      43-A (6 steps)      44-B (42)

#SEC Set 2
#K Section A   1-B   2-B   3-B   4-A   5-B   6-B   7-B   8-A   9-A   10-B
#K             11-A  12-A  13-B  14-A  15-A  16-B  17-A  18-A  19-B  20-A
#K             21-B  22-B  23-C  24-B  25-A  26-C  27-C  28-B  29-B  30-B
#K Section B   31-B  32-B  33-B  34-B  35-B  36-B  37-A  38-A  39-B  40-C
#K Section C   41-D (PLS)      42-A  8 / 4 + 3 = 5       43-C (48)           44-B (5)

#SEC Set 3
#K Section A   1-A   2-B   3-A   4-C   5-B   6-B   7-B   8-B   9-B   10-B
#K             11-B  12-A  13-B  14-A  15-A  16-B  17-B  18-B  19-B  20-B
#K             21-C  22-B  23-C  24-C  25-B  26-A  27-B  28-B  29-B  30-B
#K Section B   31-C  32-B  33-C  34-B  35-B  36-A  37-B  38-A  39-B  40-B
#K Section C   41-B (TRI)      42-B  6 * 2 - 7 = 5       43-D (95)           44-C (51)

#SEC Set 4
#K Section A   1-A   2-B   3-B   4-B   5-B   6-A   7-B   8-B   9-A   10-A
#K             11-A  12-A  13-C  14-A  15-B  16-A  17-A  18-A  19-B  20-A
#K             21-B  22-B  23-C  24-B  25-B  26-B  27-B  28-C  29-B  30-B
#K Section B   31-B  32-B  33-B  34-B  35-C  36-A  37-A  38-A  39-B  40-B
#K Section C   41-C (SQR)      42-A  3 + 4 * 6 = 27      43-C (37)           44-A (8 steps)

#SEC Set 5
#K Section A   1-B   2-A   3-B   4-A   5-B   6-B   7-C   8-B   9-B   10-A
#K             11-A  12-B  13-B  14-B  15-A  16-A  17-B  18-A  19-B  20-B
#K             21-A  22-B  23-B  24-B  25-B  26-B  27-B  28-B  29-B  30-B
#K Section B   31-B  32-B  33-B  34-B  35-C  36-A  37-A  38-A  39-A  40-B
#K Section C   41-A (CIR)      42-A  20 / 5 - 3 = 1      43-C (720)          44-C (22)

#SEC Set H1
#K Section A   1-C   2-A   3-B   4-D   5-B   6-C   7-B   8-A   9-C   10-B
#K             11-D  12-A  13-B  14-C  15-B  16-D  17-A  18-B  19-C  20-B
#K             21-B  22-B  23-C  24-C  25-C  26-B  27-B  28-C  29-B  30-B
#K Section B   31-C  32-B  33-B  34-A  35-C  36-B  37-A  38-B
#K Section C   39-B   40-C   41-A   42-A   44-A (row 3, col 3)
#K             43 Stage 2 - Yes, they are mirror images.  Stage 3 - 2 dots.

#SEC Set H2
#K Section A   1-C   2-D   3-B   4-C   5-D   6-B   7-C   8-C   9-B   10-D
#K             11-B  12-D  13-C  14-D  15-D  16-B  17-A  18-C  19-B  20-D
#K             21-B  22-B  23-B  24-B  25-C  26-C  27-D  28-C  29-B  30-C
#K Section B   31-B  32-B  33-B  34-A  35-C  36-B  37-A  38-B
#K Section C   39-C   40-D   41-B   42-A   44-A (row 1, col 2)
#K             43 Stage 2 - Yes, they are mirror images.  Stage 3 - 2 dots.

#SEC Set H3
#K Section A   1-C   2-B   3-D   4-B   5-D   6-B   7-C   8-A   9-D   10-B
#K             11-C  12-D  13-B  14-C  15-D  16-B  17-C  18-D  19-B  20-D
#K             21-B  22-C  23-A  24-B  25-B  26-B  27-B  28-B  29-B  30-B
#K Section B   31-A  32-B  33-B  34-A  35-C  36-B  37-A  38-B
#K Section C   39-C   40-B   41-D   42-C   44-B (row 5, col 3)
#K             43 Stage 2 - Option A.  Stage 3 - row 3.

#SEC Set H4
#K Section A   1-B   2-C   3-B   4-C   5-A   6-B   7-B   8-B   9-C   10-A
#K             11-B  12-B  13-A  14-B  15-C  16-C  17-C  18-A  19-A  20-A
#K             21-B  22-B  23-B  24-B  25-B  26-C  27-B  28-C  29-B  30-B
#K Section B   31-B  32-B  33-B  34-A  35-A  36-B  37-A  38-B
#K Section C   39-D   40-B   41-C   42-C   44-C (row 2, col 3)
#K             43 Stage 2 - Yes, symmetric about the main diagonal.  Stage 3 - 2 dots.

#SEC Set H5
#K Section A   1-A   2-C   3-B   4-A   5-A   6-C   7-A   8-B   9-B   10-A
#K             11-B  12-A  13-A  14-A  15-A  16-B  17-A  18-B  19-A  20-A
#K             21-B  22-B  23-B  24-B  25-B  26-B  27-B  28-B  29-A  30-D
#K Section B   31-B  32-B  33-B  34-A  35-C  36-B  37-A  38-B
#K Section C   39-C   40-B   41-B   42-A   44-B (row 4, col 4)
#K             43 Stage 2 - Option A.  Stage 3 - 2 dots.

#PB
#PART Traps Worth Reviewing
#P If you missed any of the following, the error is conceptual rather than careless, and it is worth re-tracing the item on paper before moving on.

#SUB Pass-by-value
#P Set H1 Q6 and Set H2 Q5. A function that assigns to its parameter changes nothing in the caller. In H2 Q5 the function is even named swap, which is the whole trap; x and y come back unchanged and only the returned sum reflects the internal work.

#SUB Fixed points and collapses
#P Set H4 Q9. The recurrence doubles then subtracts one, and f(1) evaluates to 1, so every later call reproduces 1. The answer is 1, not 15 or 16. Set H4 Q5 collapses to all zeros by the third iteration. Set H1 Q13 reverses the array twice, once on the first two iterations and again on the last two, returning the original order.

#SUB Integer division
#P Set 1 Q7, Set H1 Q1, Set H5 Q1. Division discards the fractional part before the next operation consumes it. In H1 Q1, c divided by b is 1 and not 1.33, which changes the entire result.

#SUB Loop exit conditions
#P Set 1 Q16, Set H2 Q3, Set H2 Q14. Count iterations by identifying when the condition first fails, not when it nearly fails. In H2 Q14 the break fires after the addition, so the loop variable has already advanced past the value you might expect.

#SUB Bit patterns versus values
#P Set H2 Q10 reverses the bit pattern of 29, giving 10111 which is 23, rather than preserving the value. Set H1 Q10 rebuilds 45 unchanged while the counter records the bit width, so the two printed values measure different things.

#SUB Binary search variants
#P Set H2 Q17 is a lower-bound search and returns the FIRST index holding the key, not any index. Set H4 Q20 finds the minimum of a rotated array and compares against A[hi], not A[lo]. Set 5 Q6 counts iterations for a key that is absent, so the loop runs to exhaustion.

#SUB Counting problems
#P Set H3 Q7 counts inversions, not comparisons. Set H3 Q19 counts the divisors of 36, which is 9, by pairing each divisor below the square root with its partner and applying the correction when i squared equals n.

#SUB Structural shortcuts
#P Set H5 Q13 relies on SILENT and LISTEN being anagrams, so the character-code sums must be equal and you never need to compute either one. Set H5 Q15 is a magic square, every row sums to 15, so the counter never increments. Set H5 Q11 prints twice, not once.

#SUB switchChallenge inversion
#P Set H2 Q40, Set H4 Q40 and Set H5 Q41 all reduce to inverting an operator rather than tracing every layer. Set H2 Q40 asks for the inverse of 3142, which is 2413. Set H4 Q40 hides the FIRST operator, so invert the given second operator to recover the intermediate row, then read off the first. Set H5 Q41 composes to the identity.

#SUB digitChallenge distinctness
#P In every digitChallenge item across all ten sets, at least one wrong option reaches the target value while reusing a digit. Set H1 Q42 option B, Set H2 Q42 option B, Set H3 Q42 option B, Set H4 Q42 option A and Set H5 Q42 options B and D are all of this kind. Screen for distinctness before you compute.

#PB
#PART Sources And Attribution
#P The assessment pattern, section structure, timings, topic coverage and band mapping in this book were compiled from the following public sources. All questions themselves are original and were written for this book; no question text was copied from any source.

#SUB Pattern, syllabus and process
#P Capgemini official Exceller page for technical graduates, capgemini.com, careers section for students and graduates.
#P PrepInsta - Capgemini Exceller syllabus and test pattern, recruitment process, coding questions, and game-based aptitude pages.
#P PlacementPreparation - Capgemini latest syllabus and test pattern, and recruitment process pages.
#P FacePrep - Capgemini pseudo-code section guide, game-based aptitude prep guide, and placement papers pages.
#P GeeksforGeeks - Capgemini pseudocode quiz bank and candidate interview experience reports.

#SUB Game mechanics
#P JobTestPrep - Aon smartPredict overview, and the individual switchChallenge, gridChallenge and digitChallenge format guides. These describe the Aon, formerly cut-e, engine that supplies the game-based section.

#SUB Important caveats
#P Capgemini does not publish official cut-offs, per-section question counts, or band criteria. Every such figure in this book is an aggregate of candidate reports and should be treated as directional rather than authoritative.
#P Sources disagree on two points. First, whether English includes a short written component; the essay writing test is reported as removed in the current pattern but is still listed by at least one source. Second, whether Python is permitted in the coding round; the more specific Exceller guidance says C, C++ and Java only. Prepare for the stricter reading of both.
#P The number of rounds, section timings and exact question counts vary by college and by drive. Confirm the format for your specific drive with your placement cell.
#P Content drawn from the sources above was rephrased for compliance with licensing restrictions.
#N This is independent practice material. It is not affiliated with, authorised by, or endorsed by Capgemini, Aon, or any assessment provider. Capgemini, Exceller, Aon, cut-e and smartPredict are trademarks of their respective owners.
"""

PARTS = [
    FRONT,
    SET1, SET2, SET3, SET4, SET5,
    HDIV,
    SETH1, SETH2, SETH3, SETH4, SETH5,
    KEYS,
]
