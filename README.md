### How to use ?

1. Open https://ai-fe-task.vercel.app/ in your browser
2. Login with credentials
   1. username: user@example.com
   2. password: 12345678
3. You will be redirected to the dashboard
4. Click on the "Search" button in the menu then enter the book id for ex. 75465
5. the book will appear as card below the search bar you can click on analysis and you will be redirected to the analysis page
6. finally  your new book will be added in my books page

### How to run locally ?

#### Backend 
1. Clone the repository
2. Run `pip install -r requirements.txt `
3. run `uvicorn app.main:app --reload`

#### Frontend 
1. Clone the repository
2. Run `npm install `
3. run `npm run dev`

### Tech Stack
1. FastAPI
2. Next.js
3. TailwindCSS

### Technical choices
1. FastAPI: I choose FastAPI because it is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints. It is easy to use and has a lot of features that make it a good choice for building APIs.
2. Next.js: I choose Next.js because it is a React framework that allows you to build static and dynamic websites and web applications. It is easy to use and has a lot of features that make it a good choice for building web applications.
3. Text analysis: 
   1. first i used spacy and text blob but it was not accurate so i used Groq as mentioned on the task description
   2. I used the Groq API to analyze the text and get the sentiment score and the entities in the text.
   3. I used specific prompt so i can split the result as i want in case future use 
4. Deployment: I choose Vercel and render because they are easy to use and have a lot of features that make it a good choice for deploying web applications.
