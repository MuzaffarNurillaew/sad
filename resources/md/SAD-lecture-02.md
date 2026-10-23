System Analysis & Design
Lecture 2
Business Information Systems

Agenda
1. Last week recap
2. Waterfall methodology
Business Information Systems 2

Recap
What did we discuss last week?
Business Information Systems 3

SDLC
1. What does SDLC stand for?
2. What are the steps in SDLC?
3. What are the 3 major categories of Software development methodologies?
Business Information Systems 4

SDLC
Planning
Implementation Analysis
Design
Business Information Systems 5

SDLC
Business Information Systems 6

Categories
There are many Software Development Models with their strengths and weaknesses. But
they can be categorized into 3 major categories:
1. Waterfall – Structured, top/down approach.
Examples: Waterfall, Structured Software Development Methodology (SSDM).
2. Iterative & Incremental – Iteratively go through important software
development “steps” (analysis, design, build, etc.) and incrementally
build the system.
Examples: Spiral, RAD, Agile, etc.
3. Prototyping – Build prototypes, get feedback, refine. Once get the
final version – build the software and deploy.
Examples: RAD, Prototyping.
Business Information Systems 7

System Develop Methodologies
| Structural: | Iterative and Incremental: | Prototyping: |
| ----------- | -------------------------- | ------------ |
• Prototyping
| • Waterfall            | • RAD    |     |
| ---------------------- | -------- | --- |
| • Structured Software  | • Spiral |     |
Development
• eXtreme Programming
Methodology (SSDM)
• Scrum
• Etc.
8

Waterfall Model
Our first SDLC methodology
Business Information Systems 9

Cost of a “bug”
Business Information Systems 10

Cost of a “bug”
Business Information Systems 11

Waterfall Model
The waterfall model is a sequential design process, used in software development
processes, in which progress is seen as flowing steadily downwards (like a waterfall)
through the phases of conception, initiation, analysis, design, construction, testing,
production/implementation and maintenance.
The waterfall development model originates in the manufacturing and construction
industries: highly structured physical environments in which after-the-fact changes are
prohibitively costly, if not impossible. Since no formal software development methodologies
existed at the time, this hardware-oriented model was simply adapted for software
development.
Business Information Systems 12

A screenshot of a computer
Description automatically generated
Business Information Systems 13

Visual representation
"Waterfall model" by Peter Kemp / Paul Smith -Adapted from Paul Smith's work at wikipedia.
Licensed under CC BY 3.0 via Commons -https://commons.wikimedia.org/wiki/File:Waterfall_model.svg#/media/File:Waterfall_model.svg
Business Information Systems 14

Model Steps
1. Requirements – Documents all requirements.
2. Design – Based on the design, build a detailed system design.
3. Implementation – Build the system based on the design.
4. Verification – Test the new system and fix all the bugs.
5. Maintenance – Deploy and maintain the system.
Business Information Systems 15

Methodology Features
• Steps are carried out in fixed order (sequencial).
• Each step must be fully finished before moving to the next (structured).
• Input of a step is the output of the previous step.
• Each step is documented. The output of each step is a documented.
Business Information Systems 16

Problems it solves
Each step has an input and output.
A step’s input is an output of the previous step.
What problems does it address?
• Changing project later on is costly. Tens or hundreds of times costly. That’s
why we need to spend time and resources to get them right at very first step.
• People may leave your team. They may be the carriers of the project related
knowledge. That’s why you need to document everything in a standard way.
• Gives concrete steps, that are easy to understand. Everyone knows at what
phase the project is, and is the main goal at the moment – synergy.
Business Information Systems 17

When to use it?
• Projects that have clearly defined final product.
• Stable and clear requirements i.e. requirements do not change.
• Clearly defined and fixed scope.
• Large scale project. For small projects it is not as effective.
What else do you think?
Business Information Systems 18

Advantages & Disadvantages
From what you have heard so far…
What are the advantages of Waterfall methodology?
We will introduce disadvantages of the model, while introducing other methodologies.
Usually, a new methodology is trying to solve specific problem in or that was not addressed
in some methodology.
Business Information Systems 19

Structured Software Development
Methodology (SSDM)
Waterfall for Information Systems development.
Business Information Systems 20

System Develop Methodologies
| Structural: | Iterative and Incremental: | Prototyping: |
| ----------- | -------------------------- | ------------ |
• Prototyping
| • Waterfall            | • RAD    |     |
| ---------------------- | -------- | --- |
| • Structured Software  | • Spiral |     |
Development
• eXtreme Programming
Methodology (SSDM)
• Scrum
• Etc.
21

SSDM
• SSDM is a Waterfall methodology for Information Systems (IS).
• It has the same “features” and follows the same ideas of Waterfall methodology:
• Structured
• Step-by-step
• Heavily promotes documentation
• Upfront planning and design
• Etc.
• SSDM was rebranded as “Business System Development” in 2000.
Business Information Systems 22

Model Steps
1. Feasibility
2. Investigation of the current environment
3. Business systems options
4. Definition of requirements
5. Technical system options
6. Logical design
7. Physical design
Business Information Systems 23

Stage 1: Feasibility
• To understand if a given project is feasible, you need to do a feasibility analysis.
• There can be different feasibility analysis:
• No feasibility – for small projects, where the environment is well
understood and no need for feasibility analysis is required.
• Informal – when the project doesn’t have enough time or resources to
spend, and it does not require documenting feasibility process.
• Formal – you talk to users, identify business needs, problems,
requirements and document it all in feasibility analysis report. This
usually requires you to do initial requirements gathering.
Business Information Systems 24

Stage 1: Feasibility
Concentrate on these areas:
• Technical – Is this project technically possible?
• Financial – Can the business effort it? Hardware, software, licenses, salaries for new
staff, etc.
• Organizational – Will the organization adopt the new system? Is an organization
willing to change/reorganize?
• Ethical – Will the final product raise ethical issues?
Also, don’t forget to document the unfeasible, rejected solutions or versions of the project.
Business Information Systems 25

Stage 2: Investigate the current env
• One of the most important stages. This helps the system analyst to understand the
current user needs and problems.
• There are different techniques that you may employ:
• Current system analysis
• Read documentation
• Interview
• Questionnaires
• Surveys
• etc. (we will talk more about these techniques in a separate lecture)
Business Information Systems 26

Stage 3: Business system options
• Equipped with the understanding of the current system in Stage 2, System Analyst tries to
generate different “options” of the new system.
• Possible options:
• Don’t do anything, leave the old system, everything is great.
• Leave the old system, change business/operational rules.
• Improve the existing system.
• …
• As the last resort – create a new system from scratch.
Business Information Systems 27

Stage 3: Business system options
• You should try to get as many ideas and options as you can.
• Compile several “options” taking into the consideration all the information you gathered in
previous stages.
• Can the business afford this option?
• Will it suite the organization?
• Will users use it?
• What changes must be made in organization?
• etc.
• The product of this stage is (a single) chosen option.
Business Information Systems 28

Stage 4: Definition of requirements
• Defines concrete, unambiguous and concise system requirements.
• At this stage you should produce:
a) Logical Data Model – what the system will do, not how.
b) Data Flow Diagram – what data is essential and its’ relations.
c) Entity Event Model – what are system actions and how they change the data in it?
Business Information Systems 29

Stage 4: Definition of requirements
Logical Data Model Example:
Source: http://www.conceptdraw.com/solution-park/resource/images/solutions/entity-relationship-diagram-(erd)/Diagramming-Crow's-Foot-ERD-Sample60.png
Business Information Systems 30

Stage 4: Definition of requirements
Data Flow Diagram Example:
Source: http://www.jscgroup.com/images/ch-426-s.jpg
Business Information Systems 31

Stage 5: Technical system options
• As in “Business system option” stage, you try to come up with several options to
implement the new system. But, this time it is about technical aspects of the system.
• At the end, you would decide which “technical option” will be used.
Source: http://www.jscgroup.com/images/ch-426-s.jpg
Business Information Systems 32

Stage 5: Technical system options
You might want to consider:
• What software will you use?
• What programming language?
• Hardware architecture
• Network architecture
• The cost of an option
• etc.
Source: http://www.jscgroup.com/images/ch-426-s.jpg
Business Information Systems 33

Stage 6: Logical Design
• This step identifies and produces the specification on how users will interact with the
system.
• In practice this means User Interface (UI).
• What techniques can you use at this stage?
Source: http://www.jscgroup.com/images/ch-426-s.jpg
Business Information Systems 34

Stage 7: Physical design
• The final stage, where the system is physically implemented.
• Uses Logical Design stage outputs as an input. UI elements inherently contain business
requirements defined in earlier stages.
• Output is the working system.
Source: http://www.jscgroup.com/images/ch-426-s.jpg
Business Information Systems 35

Methodology Features
The same as in Waterfall:
• Steps are carried out in fixed order (sequencial).
• Each step must be fully finished before moving to the next (structured).
• Input of a step is the output of the previous step.
• Each step is documented. The output of each step is a documented.
Business Information Systems 36

Problems it solves
Each step has an input and output.
A step’s input is an output of the previous step.
What problems does it address?
• Changing project later on is costly. Tens or hundreds of times costly. That’s
why we need to spend time and resources to get them right at very first step.
• People may leave your team. They may be the carriers of the project related
knowledge. That’s why you need to document everything in a standard way.
• Gives concrete steps, that are easy to understand. Everyone knows at what
phase the project is, and is the main goal at the moment – synergy.
Business Information Systems 37

When to use it?
• Projects that have clearly defined final product.
• Stable and clear requirements i.e. requirements do not change.
• Clearly defined and fixed scope.
• Large scale project. For small projects it is not as effective.
What else do you think?
Business Information Systems 38

Structured Software Development
Methodology (SSDM)
Waterfall for Information Systems development.
Business Information Systems 39

Questions?
Business Information Systems 40

The End
Business Information Systems 41
