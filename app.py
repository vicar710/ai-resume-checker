import time
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.add_vertical_space import add_vertical_space
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
import google.generativeai as genai
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import warnings
warnings.filterwarnings('ignore')


def streamlit_config():

    # page configuration
    st.set_page_config(page_title='Resume Analyzer AI', layout="wide")

    # page header transparent color
    page_background_color = """
    <style>

    [data-testid="stHeader"] 
    {
    background: rgba(0,0,0,0);
    }

    </style>
    """
    st.markdown(page_background_color, unsafe_allow_html=True)

    # title and position
    st.markdown(f'<h1 style="text-align: center;">Resume Analyzer AI</h1>',
                unsafe_allow_html=True)


class resume_analyzer:

    def pdf_to_chunks(pdf):
        # read pdf and it returns memory address
        pdf_reader = PdfReader(pdf)

        # extrat text from each page separately
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        # Split the long text into small chunks.
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=700,
            chunk_overlap=200,
            length_function=len)

        chunks = text_splitter.split_text(text=text)
        return chunks


    def gemini(gemini_api_key, chunks, analyze):

        # Configure Google Generative AI
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("models/gemini-2.5-flash")

        # Using Google Gemini service for embedding
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=gemini_api_key)

        # Facebook AI Similarity Serach library help us to convert text data to numerical vector
        vectorstores = FAISS.from_texts(chunks, embedding=embeddings)

        # compares the query and chunks, enabling the selection of the top 'K' most similar chunks based on their similarity scores.
        docs = vectorstores.similarity_search(query=analyze, k=3)

        # Prepare context from retrieved documents
        context = "\n".join([doc.page_content for doc in docs])
        
        # Create prompt with context and question
        prompt = f"""Based on the following context, please answer the question:

Context:
{context}

Question: {analyze}

Please provide a detailed and helpful response based on the context provided."""

        # Generate response using Gemini 1.5 Flash
        response = model.generate_content(prompt)
        return response.text


    def summary_prompt(query_with_chunks):

        query = f''' need to detailed summarization of below resume and finally conclude them

                    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    {query_with_chunks}
                    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    '''
        return query


    def resume_summary():

        with st.form(key='Summary'):

            # User Upload the Resume
            add_vertical_space(1)
            pdf = st.file_uploader(label='Upload Your Resume', type='pdf')
            add_vertical_space(1)

            # Enter Google Gemini API Key
            col1,col2 = st.columns([0.6,0.4])
            with col1:
                gemini_api_key = st.text_input(label='Enter Google Gemini API Key', type='password')
            add_vertical_space(2)

            # Click on Submit Button
            submit = st.form_submit_button(label='Submit')
            add_vertical_space(1)
        
        add_vertical_space(3)
        if submit:
            if pdf is not None and gemini_api_key != '':
                try:
                    with st.spinner('Processing...'):

                        pdf_chunks = resume_analyzer.pdf_to_chunks(pdf)

                        summary_prompt = resume_analyzer.summary_prompt(query_with_chunks=pdf_chunks)

                        summary = resume_analyzer.gemini(gemini_api_key=gemini_api_key, chunks=pdf_chunks, analyze=summary_prompt)

                    st.markdown(f'<h4 style="color: orange;">Summary:</h4>', unsafe_allow_html=True)
                    st.write(summary)

                except Exception as e:
                    st.markdown(f'<h5 style="text-align: center;color: orange;">{e}</h5>', unsafe_allow_html=True)

            elif pdf is None:
                st.markdown(f'<h5 style="text-align: center;color: orange;">Please Upload Your Resume</h5>', unsafe_allow_html=True)
            
            elif gemini_api_key == '':
                st.markdown(f'<h5 style="text-align: center;color: orange;">Please Enter Google Gemini API Key</h5>', unsafe_allow_html=True)


    def strength_prompt(query_with_chunks):
        query = f'''need to detailed analysis and explain of the strength of below resume and finally conclude them
                    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    {query_with_chunks}
                    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    '''
        return query


    def resume_strength():

        with st.form(key='Strength'):

            # User Upload the Resume
            add_vertical_space(1)
            pdf = st.file_uploader(label='Upload Your Resume', type='pdf')
            add_vertical_space(1)

            # Enter Google Gemini API Key
            col1,col2 = st.columns([0.6,0.4])
            with col1:
                gemini_api_key = st.text_input(label='Enter Google Gemini API Key', type='password')
            add_vertical_space(2)

            # Click on Submit Button
            submit = st.form_submit_button(label='Submit')
            add_vertical_space(1)

        add_vertical_space(3)
        if submit:
            if pdf is not None and gemini_api_key != '':
                try:
                    with st.spinner('Processing...'):
                    
                        pdf_chunks = resume_analyzer.pdf_to_chunks(pdf)

                        summary_prompt = resume_analyzer.summary_prompt(query_with_chunks=pdf_chunks)

                        summary = resume_analyzer.gemini(gemini_api_key=gemini_api_key, chunks=pdf_chunks, analyze=summary_prompt)
                        
                        strength_prompt = resume_analyzer.strength_prompt(query_with_chunks=summary)

                        strength = resume_analyzer.gemini(gemini_api_key=gemini_api_key, chunks=pdf_chunks, analyze=strength_prompt)

                    st.markdown(f'<h4 style="color: orange;">Strength:</h4>', unsafe_allow_html=True)
                    st.write(strength)

                except Exception as e:
                    st.markdown(f'<h5 style="text-align: center;color: orange;">{e}</h5>', unsafe_allow_html=True)

            elif pdf is None:
                st.markdown(f'<h5 style="text-align: center;color: orange;">Please Upload Your Resume</h5>', unsafe_allow_html=True)
            
            elif gemini_api_key == '':
                st.markdown(f'<h5 style="text-align: center;color: orange;">Please Enter Google Gemini API Key</h5>', unsafe_allow_html=True)


    def weakness_prompt(query_with_chunks):
        query = f'''need to detailed analysis and explain of the weakness of below resume and how to improve make a better resume.

                    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    {query_with_chunks}
                    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    '''
        return query


    def resume_weakness():

        with st.form(key='Weakness'):

            # User Upload the Resume
            add_vertical_space(1)
            pdf = st.file_uploader(label='Upload Your Resume', type='pdf')
            add_vertical_space(1)

            # Enter Google Gemini API Key
            col1,col2 = st.columns([0.6,0.4])
            with col1:
                gemini_api_key = st.text_input(label='Enter Google Gemini API Key', type='password')
            add_vertical_space(2)

            # Click on Submit Button
            submit = st.form_submit_button(label='Submit')
            add_vertical_space(1)
        
        add_vertical_space(3)
        if submit:
            if pdf is not None and gemini_api_key != '':
                try:
                    with st.spinner('Processing...'):
                    
                        pdf_chunks = resume_analyzer.pdf_to_chunks(pdf)

                        summary_prompt = resume_analyzer.summary_prompt(query_with_chunks=pdf_chunks)

                        summary = resume_analyzer.gemini(gemini_api_key=gemini_api_key, chunks=pdf_chunks, analyze=summary_prompt)

                        weakness_prompt = resume_analyzer.weakness_prompt(query_with_chunks=summary)

                        weakness = resume_analyzer.gemini(gemini_api_key=gemini_api_key, chunks=pdf_chunks, analyze=weakness_prompt)

                    st.markdown(f'<h4 style="color: orange;">Weakness and Suggestions:</h4>', unsafe_allow_html=True)
                    st.write(weakness)

                except Exception as e:
                    st.markdown(f'<h5 style="text-align: center;color: orange;">{e}</h5>', unsafe_allow_html=True)

            elif pdf is None:
                st.markdown(f'<h5 style="text-align: center;color: orange;">Please Upload Your Resume</h5>', unsafe_allow_html=True)
            
            elif gemini_api_key == '':
                st.markdown(f'<h5 style="text-align: center;color: orange;">Please Enter Google Gemini API Key</h5>', unsafe_allow_html=True)


    def job_title_prompt(query_with_chunks):

        query = f''' what are the job roles i apply to likedin based on below?
                    
                    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    {query_with_chunks}
                    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    '''
        return query


    def job_title_suggestion():

        with st.form(key='Job Titles'):

            # User Upload the Resume
            add_vertical_space(1)
            pdf = st.file_uploader(label='Upload Your Resume', type='pdf')
            add_vertical_space(1)

            # Enter Google Gemini API Key
            col1,col2 = st.columns([0.6,0.4])
            with col1:
                gemini_api_key = st.text_input(label='Enter Google Gemini API Key', type='password')
            add_vertical_space(2)

            # Click on Submit Button
            submit = st.form_submit_button(label='Submit')
            add_vertical_space(1)

        add_vertical_space(3)
        if submit:
            if pdf is not None and gemini_api_key != '':
                try:
                    with st.spinner('Processing...'):
                    
                        pdf_chunks = resume_analyzer.pdf_to_chunks(pdf)

                        summary_prompt = resume_analyzer.summary_prompt(query_with_chunks=pdf_chunks)

                        summary = resume_analyzer.gemini(gemini_api_key=gemini_api_key, chunks=pdf_chunks, analyze=summary_prompt)

                        job_title_prompt = resume_analyzer.job_title_prompt(query_with_chunks=summary)

                        job_title = resume_analyzer.gemini(gemini_api_key=gemini_api_key, chunks=pdf_chunks, analyze=job_title_prompt)

                    st.markdown(f'<h4 style="color: orange;">Job Titles:</h4>', unsafe_allow_html=True)
                    st.write(job_title)

                except Exception as e:
                    st.markdown(f'<h5 style="text-align: center;color: orange;">{e}</h5>', unsafe_allow_html=True)

            elif pdf is None:
                st.markdown(f'<h5 style="text-align: center;color: orange;">Please Upload Your Resume</h5>', unsafe_allow_html=True)
            
            elif gemini_api_key == '':
                st.markdown(f'<h5 style="text-align: center;color: orange;">Please Enter Google Gemini API Key</h5>', unsafe_allow_html=True)



    def _preprocess_text(text):
        words = ''.join([c.lower() if c.isalnum() or c.isspace() else ' ' for c in text]).split()
        stopwords = {
            'and','or','the','a','an','to','of','in','on','for','with','at','by','from','as','is','are','was','were','be','been','being','that','this','it','its','into','your','you','we','our','their','they','i','me','my','mine','us','about','over','under','per','via','using'
        }
        return [w for w in words if len(w) > 2 and w not in stopwords]

    def _keywords(text):
        tokens = resume_analyzer._preprocess_text(text)
        return set(tokens)

    def _ats_prompt(resume_text, job_desc, overlap_keywords, missing_keywords, score):
        return f"""
You are an ATS optimization assistant. Given a candidate resume and a target job description, provide concrete improvements to increase ATS keyword alignment and clarity.

Resume:
{resume_text[:8000]}

Job Description:
{job_desc[:8000]}

Current keyword match score: {score:.1f}%
Matched keywords: {', '.join(sorted(list(overlap_keywords)))}
Missing high-impact keywords: {', '.join(sorted(list(missing_keywords)))}

Please output:
1) The top sections/lines to tweak.
2) Bullet edits to naturally include missing keywords.
3) A short summary paragraph tailored to the JD.
"""

    def ats_checker():

        with st.form(key='ATS'):
            add_vertical_space(1)
            pdf = st.file_uploader(label='Upload Your Resume', type='pdf')
            add_vertical_space(1)

            col1, col2 = st.columns([0.6,0.4])
            with col1:
                job_desc = st.text_area(label='Paste Target Job Description', height=220)
            with col2:
                gemini_api_key = st.text_input(label='Enter Google Gemini API Key (optional for suggestions)', type='password')
            add_vertical_space(2)

            submit = st.form_submit_button(label='Run ATS Check')
            add_vertical_space(1)

        add_vertical_space(2)
        if submit:
            if pdf is None:
                st.markdown(f'<h5 style="text-align: center;color: orange;">Please Upload Your Resume</h5>', unsafe_allow_html=True)
                return
            if job_desc.strip() == '':
                st.markdown(f'<h5 style="text-align: center;color: orange;">Please Paste a Job Description</h5>', unsafe_allow_html=True)
                return

            try:
                with st.spinner('Processing...'):
                    pdf_reader = PdfReader(pdf)
                    resume_text = ''
                    for page in pdf_reader.pages:
                        resume_text += page.extract_text() or ''

                    resume_keywords = resume_analyzer._keywords(resume_text)
                    jd_keywords = resume_analyzer._keywords(job_desc)

                    overlap = resume_keywords.intersection(jd_keywords)
                    missing = jd_keywords.difference(resume_keywords)
                    score = (len(overlap) / max(1, len(jd_keywords))) * 100.0

                st.markdown(f'<h4 style="color: orange;">ATS Score:</h4>', unsafe_allow_html=True)
                st.write(f"{score:.1f}% keyword match")

                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f'<h5 style="color: orange;">Matched Keywords</h5>', unsafe_allow_html=True)
                    st.write(', '.join(sorted(list(overlap))) if overlap else 'None')
                with col_b:
                    st.markdown(f'<h5 style="color: orange;">Missing Keywords</h5>', unsafe_allow_html=True)
                    st.write(', '.join(sorted(list(missing))) if missing else 'None')

                if gemini_api_key.strip() != '':
                    with st.spinner('Generating optimization suggestions...'):
                        chunks = resume_analyzer.pdf_to_chunks(pdf)
                        prompt = resume_analyzer._ats_prompt(resume_text, job_desc, overlap, missing, score)
                        suggestions = resume_analyzer.gemini(gemini_api_key=gemini_api_key, chunks=chunks, analyze=prompt)
                    st.markdown(f'<h4 style="color: orange;">Suggestions to Improve ATS Fit:</h4>', unsafe_allow_html=True)
                    st.write(suggestions)

            except Exception as e:
                st.markdown(f'<h5 style="text-align: center;color: orange;">{e}</h5>', unsafe_allow_html=True)


    def _faang_profiles():
        return {
            'Meta': {
                'core': {
                    'software','engineer','backend','frontend','fullstack','distributed','systems','scalability','reliability','performance',
                    'api','microservices','rest','grpc','react','reactjs','react-native','hack','php','python','java','c++','csharp','typescript',
                    'graphql','kafka','spark','hadoop','hive','presto','ml','machine','learning','ranking','recommendation','recommendations',
                    'feature','flags','experiment','ab','a/b','security','privacy','datastore','mysql','rocksdb','cassandra','thrift','orc',
                    'observability','metrics','tracing','logging','sre','ci','cd','kubernetes','docker','cloud'
                }
            },
            'Apple': {
                'core': {
                    'software','ios','swift','objective-c','macos','swiftui','uikit','coredata','combine','xcode','design','human','interface',
                    'privacy','security','hardware','firmware','embedded','bluetooth','wifi','driver','performance','battery','latency','metal',
                    'graphics','ml','coreml','vision','nlp','siri','framework','sdk','api','qa','automation','accessibility'
                }
            },
            'Amazon': {
                'core': {
                    'software','services','aws','lambda','dynamodb','s3','ec2','sqs','sns','aurora','rds','redshift','kinesis','emr','glue',
                    'microservices','java','python','scala','c++','distributed','systems','ownership','bar','raiser','operational','excellence',
                    'metrics','slo','oncall','paging','security','iam','cost','optimization','api','rest','grpc','graphql','serverless'
                }
            },
            'Netflix': {
                'core': {
                    'java','groovy','kotlin','spring','rxjava','reactive','microservices','spinnaker','chaos','engineering','eureka','zuul',
                    'rest','cloud','aws','s3','ec2','sqs','kinesis','observability','atlas','spectator','governance','resilience','performance',
                    'cdn','encoding','streaming','ab','experimentation','personalization','recommendation'
                }
            },
            'Google': {
                'core': {
                    'software','engineer','c++','java','python','go','golang','mapreduce','bigtable','spanner','borg','kubernetes','grpc',
                    'protocol','buffers','protobuf','ml','tensorflow','jax','tpu','search','ranking','indexing','information','retrieval',
                    'distributed','systems','sre','reliability','latency','throughput','rpc','compiler','algorithms','data','structures'
                }
            }
        }

    def _faang_prompt(resume_text, company, overlap_keywords, missing_keywords, score):
        return f"""
Act as a hiring engineer at {company}. Improve the candidate resume for better fit.

Resume:
{resume_text[:8000]}

Current keyword match score to {company}: {score:.1f}%
Matched keywords: {', '.join(sorted(list(overlap_keywords)))}
Missing high-impact keywords for {company}: {', '.join(sorted(list(missing_keywords)))}

Provide:
1) Specific bullet edits to naturally include missing keywords (no fluff).
2) One strong resume summary tailored for {company}.
3) Optional: brief project bullets that evidence the missing skills.
"""

    def faang_match():

        with st.form(key='FAANG'):
            add_vertical_space(1)
            pdf = st.file_uploader(label='Upload Your Resume', type='pdf')
            add_vertical_space(1)

            profiles = resume_analyzer._faang_profiles()
            companies = list(profiles.keys())
            sel = st.multiselect('Select companies', companies, default=companies)

            col1, col2 = st.columns([0.6,0.4])
            with col1:
                role_hint = st.text_input('Optional: Target role (e.g., Backend, iOS, ML)')
            with col2:
                gemini_api_key = st.text_input(label='Enter Google Gemini API Key (optional for suggestions)', type='password')
            add_vertical_space(2)

            submit = st.form_submit_button(label='Run FAANG Match')
            add_vertical_space(1)

        add_vertical_space(2)
        if submit:
            if pdf is None:
                st.markdown(f'<h5 style="text-align: center;color: orange;">Please Upload Your Resume</h5>', unsafe_allow_html=True)
                return
            if sel == []:
                st.markdown(f'<h5 style="text-align: center;color: orange;">Please select at least one company</h5>', unsafe_allow_html=True)
                return

            try:
                with st.spinner('Processing...'):
                    pdf_reader = PdfReader(pdf)
                    resume_text = ''
                    for page in pdf_reader.pages:
                        resume_text += page.extract_text() or ''

                    resume_kw = resume_analyzer._keywords(resume_text)

                    results = []
                    for c in sel:
                        base_kw = set(profiles[c]['core'])
                        # If user hinted a role, bias by injecting hint terms into base keywords
                        if role_hint.strip() != '':
                            base_kw = base_kw.union(resume_analyzer._keywords(role_hint))

                        overlap = resume_kw.intersection(base_kw)
                        missing = base_kw.difference(resume_kw)
                        score = (len(overlap) / max(1, len(base_kw))) * 100.0
                        results.append((c, score, overlap, missing))

                # Display table of scores
                st.markdown(f'<h4 style="color: orange;">FAANG Match Scores</h4>', unsafe_allow_html=True)
                df_scores = pd.DataFrame(
                    [{'Company': c, 'Score %': round(s,1), 'Matched': len(o), 'Missing': len(m)} for c, s, o, m in results]
                ).sort_values('Score %', ascending=False).reset_index(drop=True)
                st.dataframe(df_scores, use_container_width=True)

                # Details per company
                for c, s, o, m in results:
                    with st.expander(f'{c} details — {s:.1f}%'):
                        colx, coly = st.columns(2)
                        with colx:
                            st.markdown(f'<h5 style="color: orange;">Matched</h5>', unsafe_allow_html=True)
                            st.write(', '.join(sorted(list(o))) if o else 'None')
                        with coly:
                            st.markdown(f'<h5 style="color: orange;">Missing</h5>', unsafe_allow_html=True)
                            st.write(', '.join(sorted(list(m))) if m else 'None')

                        if gemini_api_key.strip() != '':
                            with st.spinner(f'Generating {c} suggestions...'):
                                chunks = resume_analyzer.pdf_to_chunks(pdf)
                                prompt = resume_analyzer._faang_prompt(resume_text, c, o, m, s)
                                suggestions = resume_analyzer.gemini(gemini_api_key=gemini_api_key, chunks=chunks, analyze=prompt)
                            st.markdown(f'<h5 style="color: orange;">Suggestions</h5>', unsafe_allow_html=True)
                            st.write(suggestions)

            except Exception as e:
                st.markdown(f'<h5 style="text-align: center;color: orange;">{e}</h5>', unsafe_allow_html=True)
class linkedin_scraper:

    def webdriver_setup():
            
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        return driver


    def get_userinput():

        add_vertical_space(2)
        with st.form(key='linkedin_scarp'):

            add_vertical_space(1)
            col1,col2,col3 = st.columns([0.5,0.3,0.2], gap='medium')
            with col1:
                job_title_input = st.text_input(label='Job Title')
                job_title_input = job_title_input.split(',')
            with col2:
                job_location = st.text_input(label='Job Location', value='India')
            with col3:
                job_count = st.number_input(label='Job Count', min_value=1, value=1, step=1)

            # Submit Button
            add_vertical_space(1)
            submit = st.form_submit_button(label='Submit')
            add_vertical_space(1)
        
        return job_title_input, job_location, job_count, submit


    def build_url(job_title, job_location):

        b = []
        for i in job_title:
            x = i.split()
            y = '%20'.join(x)
            b.append(y)

        job_title = '%2C%20'.join(b)
        link = f"https://in.linkedin.com/jobs/search?keywords={job_title}&location={job_location}&locationId=&geoId=102713980&f_TPR=r604800&position=1&pageNum=0"

        return link
    

    def open_link(driver, link):

        while True:
            # Break the Loop if the Element is Found, Indicating the Page Loaded Correctly
            try:
                driver.get(link)
                driver.implicitly_wait(5)
                time.sleep(3)
                driver.find_element(by=By.CSS_SELECTOR, value='span.switcher-tabs__placeholder-text.m-auto')
                return
            
            # Retry Loading the Page
            except NoSuchElementException:
                continue


    def link_open_scrolldown(driver, link, job_count):
        
        # Open the Link in LinkedIn
        linkedin_scraper.open_link(driver, link)

        # Scroll Down the Page
        for i in range(0,job_count):

            # Simulate clicking the Page Up button
            body = driver.find_element(by=By.TAG_NAME, value='body')
            body.send_keys(Keys.PAGE_UP)

            # Locate the sign-in modal dialog 
            try:
                driver.find_element(by=By.CSS_SELECTOR, 
                                value="button[data-tracking-control-name='public_jobs_contextual-sign-in-modal_modal_dismiss']>icon>svg").click()
            except:
                pass

            # Scoll down the Page to End
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.implicitly_wait(2)

            # Click on See More Jobs Button if Present
            try:
                x = driver.find_element(by=By.CSS_SELECTOR, value="button[aria-label='See more jobs']").click()
                driver.implicitly_wait(5)
            except:
                pass


    def job_title_filter(scrap_job_title, user_job_title_input):
        
        # User Job Title Convert into Lower Case
        user_input = [i.lower().strip() for i in user_job_title_input]

        # scraped Job Title Convert into Lower Case
        scrap_title = [i.lower().strip() for i in [scrap_job_title]]

        # Verify Any User Job Title in the scraped Job Title
        confirmation_count = 0
        for i in user_input:
            if all(j in scrap_title[0] for j in i.split()):
                confirmation_count += 1

        # Return Job Title if confirmation_count greater than 0 else return NaN
        if confirmation_count > 0:
            return scrap_job_title
        else:
            return np.nan


    def scrap_company_data(driver, job_title_input, job_location):

        # scraping the Company Data
        company = driver.find_elements(by=By.CSS_SELECTOR, value='h4[class="base-search-card__subtitle"]')
        company_name = [i.text for i in company]

        location = driver.find_elements(by=By.CSS_SELECTOR, value='span[class="job-search-card__location"]')
        company_location = [i.text for i in location]

        title = driver.find_elements(by=By.CSS_SELECTOR, value='h3[class="base-search-card__title"]')
        job_title = [i.text for i in title]

        url = driver.find_elements(by=By.XPATH, value='//a[contains(@href, "/jobs/")]')
        website_url = [i.get_attribute('href') for i in url]

        # combine the all data to single dataframe
        df = pd.DataFrame(company_name, columns=['Company Name'])
        df['Job Title'] = pd.DataFrame(job_title)
        df['Location'] = pd.DataFrame(company_location)
        df['Website URL'] = pd.DataFrame(website_url)

        # Return Job Title if there are more than 1 matched word else return NaN
        df['Job Title'] = df['Job Title'].apply(lambda x: linkedin_scraper.job_title_filter(x, job_title_input))

        # Return Location if User Job Location in Scraped Location else return NaN
        df['Location'] = df['Location'].apply(lambda x: x if job_location.lower() in x.lower() else np.nan)
        
        # Drop Null Values and Reset Index
        df = df.dropna()
        df.reset_index(drop=True, inplace=True)

        return df 
        

    def scrap_job_description(driver, df, job_count):
        
        # Get URL into List
        website_url = df['Website URL'].tolist()
        
        # Scrap the Job Description
        job_description = []
        description_count = 0

        for i in range(0, len(website_url)):
            try:
                # Open the Link in LinkedIn
                linkedin_scraper.open_link(driver, website_url[i])

                # Click on Show More Button
                driver.find_element(by=By.CSS_SELECTOR, value='button[data-tracking-control-name="public_jobs_show-more-html-btn"]').click()
                driver.implicitly_wait(5)
                time.sleep(1)

                # Get Job Description
                description = driver.find_elements(by=By.CSS_SELECTOR, value='div[class="show-more-less-html__markup relative overflow-hidden"]')
                data = [i.text for i in description][0]
                
                # Check Description length and Duplicate
                if len(data.strip()) > 0 and data not in job_description:
                    job_description.append(data)
                    description_count += 1
                else:
                    job_description.append('Description Not Available')
            
            # If any unexpected issue 
            except:
                job_description.append('Description Not Available')
            
            # Check Description Count reach User Job Count
            if description_count == job_count:
                break

        # Filter the Job Description
        df = df.iloc[:len(job_description), :]

        # Add Job Description in Dataframe
        df['Job Description'] = pd.DataFrame(job_description, columns=['Description'])
        df['Job Description'] = df['Job Description'].apply(lambda x: np.nan if x=='Description Not Available' else x)
        df = df.dropna()
        df.reset_index(drop=True, inplace=True)
        return df


    def display_data_userinterface(df_final):

        # Display the Data in User Interface
        add_vertical_space(1)
        if len(df_final) > 0:
            for i in range(0, len(df_final)):
                
                st.markdown(f'<h3 style="color: orange;">Job Posting Details : {i+1}</h3>', unsafe_allow_html=True)
                st.write(f"Company Name : {df_final.iloc[i,0]}")
                st.write(f"Job Title    : {df_final.iloc[i,1]}")
                st.write(f"Location     : {df_final.iloc[i,2]}")
                st.write(f"Website URL  : {df_final.iloc[i,3]}")

                with st.expander(label='Job Desription'):
                    st.write(df_final.iloc[i, 4])
                add_vertical_space(3)
        
        else:
            st.markdown(f'<h5 style="text-align: center;color: orange;">No Matching Jobs Found</h5>', 
                                unsafe_allow_html=True)


    def main():
        
        # Initially set driver to None
        driver = None
        
        try:
            job_title_input, job_location, job_count, submit = linkedin_scraper.get_userinput()
            add_vertical_space(2)
            
            if submit:
                if job_title_input != [] and job_location != '':
                    
                    with st.spinner('Chrome Webdriver Setup Initializing...'):
                        driver = linkedin_scraper.webdriver_setup()
                                       
                    with st.spinner('Loading More Job Listings...'):

                        # build URL based on User Job Title Input
                        link = linkedin_scraper.build_url(job_title_input, job_location)

                        # Open the Link in LinkedIn and Scroll Down the Page
                        linkedin_scraper.link_open_scrolldown(driver, link, job_count)

                    with st.spinner('scraping Job Details...'):

                        # Scraping the Company Name, Location, Job Title and URL Data
                        df = linkedin_scraper.scrap_company_data(driver, job_title_input, job_location)

                        # Scraping the Job Descriptin Data
                        df_final = linkedin_scraper. scrap_job_description(driver, df, job_count)
                    
                    # Display the Data in User Interface
                    linkedin_scraper.display_data_userinterface(df_final)

                
                # If User Click Submit Button and Job Title is Empty
                elif job_title_input == []:
                    st.markdown(f'<h5 style="text-align: center;color: orange;">Job Title is Empty</h5>', 
                                unsafe_allow_html=True)
                
                elif job_location == '':
                    st.markdown(f'<h5 style="text-align: center;color: orange;">Job Location is Empty</h5>', 
                                unsafe_allow_html=True)

        except Exception as e:
            add_vertical_space(2)
            st.markdown(f'<h5 style="text-align: center;color: orange;">{e}</h5>', unsafe_allow_html=True)
        
        finally:
            if driver:
                driver.quit()



# Streamlit Configuration Setup
streamlit_config()
add_vertical_space(2)



with st.sidebar:

    add_vertical_space(4)

    option = option_menu(menu_title='', options=['Summary', 'Strength', 'Weakness', 'Job Titles', 'ATS Checker', 'FAANG Match', 'Linkedin Jobs'],
                         icons=['house-fill', 'database-fill', 'pass-fill', 'list-ul', 'check2-circle', 'star-fill', 'linkedin'])



if option == 'Summary':

    resume_analyzer.resume_summary()



elif option == 'Strength':

    resume_analyzer.resume_strength()



elif option == 'Weakness':

    resume_analyzer.resume_weakness()



elif option == 'Job Titles':

    resume_analyzer.job_title_suggestion()



elif option == 'ATS Checker':

    resume_analyzer.ats_checker()



elif option == 'FAANG Match':

    resume_analyzer.faang_match()



elif option == 'Linkedin Jobs':
    
    linkedin_scraper.main()


