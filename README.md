# Private_Offline_GPT
I've created a chatbot application using generative AI technology, which is built upon the open-source tools and packages Llama and GPT4All. This application represents my own work and was developed by integrating these tools, and it adopts a chat-based interface. It shares a framework with PrivateGPT, inspired by imartinez's PrivateGPT,

1)  Install the requirements
2)  Download the model you prefer from https://gpt4all.io/index.html and place it in the models folder
3)  Make necessary changes 
4)  Add your documents from which you have to do question answering into the source documnets folder 
5)  Run Ingest.py
6)  This will create a GPT Vector index inside the db folder 
7)  Now run app.py 
      streamlit run app.py
