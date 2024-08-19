from langchain.text_splitter import CharacterTextSplitter
import json
import os
import random
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import google.generativeai as genai
import nltk
import pandas as pd
from groq import Groq
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_cohere import CohereRerank
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import UnstructuredCSVLoader
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.document_loaders import UnstructuredPowerPointLoader
from langchain_community.document_loaders import UnstructuredXMLLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.llms import Cohere
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from typing import List
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('punkt')

def process_json_file(file_path):
    json_data = []
    with open(file_path, 'r') as file:
        for line in file:
            try:
                data = json.loads(line)
                json_data.append(data)
            except json.JSONDecodeError:
                try:
                    data = json.loads(line[:-1])
                    json_data.append(data)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
    return json_data

from dotenv import load_dotenv
import os
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY1= os.getenv("GOOGLE_API_KEY_1")
GOOGLE_API_KEY= os.getenv("GOOGLE_API_KEY")
os.environ["COHERE_API_KEY"] = COHERE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
client = Groq(
    api_key= GROQ_API_KEY,
)
genai.configure(api_key=GOOGLE_API_KEY1)
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", task_type="retrieval_document")
llm = ChatGoogleGenerativeAI(model='gemini-pro',
                             max_output_tokens=2048,
                             temperature=0.2,
                             convert_system_message_to_human=True)
def extract_multi_metadata_content(texts, tests):
    extracted_content = []
    precomputed_metadata = [x.metadata['source'].lower() for x in texts]
    for idx, test in enumerate(tests):
        temp_content = []
        test_terms = set(test.lower().split())
        for metadata_lower, x in zip(precomputed_metadata, texts):
            if any(term in metadata_lower for term in test_terms):
                temp_content.append(x.page_content)
        if idx == 0:
            extracted_content.append(f"Dữ liệu của {test}:\n{''.join(temp_content)}")
        else:
            extracted_content.append(''.join(temp_content))
    return '\n'.join(extracted_content)
import unicodedata
def text_preprocessing(text):
    text = text.lower()
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    text = unicodedata.normalize('NFC', text)
    words = text.split()
    text = ' '.join(words)
    return text
def find_matching_files_in_docs_12_id(text, id):
    folder_path = f"./user_file/{id}"
    search_terms = []
    search_terms_old = []
    matching_index = []
    search_origin = re.findall(r'\b\w+\.\w+\b|\b\w+\b', text)
    search_terms_origin = []
    for word in search_origin:
        if '.' in word:
            search_terms_origin.append(word)
        else:
            search_terms_origin.extend(re.findall(r'\b\w+\b', word))

    file_names_with_extension = re.findall(r'\b\w+\.\w+\b|\b\w+\b', text.lower())
    file_names_with_extension_old = re.findall(r'\b(\w+\.\w+)\b', text)
    for file_name in search_terms_origin:
        if "." in file_name:
            search_terms_old.append(file_name)
    for file_name in file_names_with_extension_old:
        if "." in file_name:
            search_terms_old.append(file_name)
    for file_name in file_names_with_extension:
        search_terms.append(file_name)
    clean_text_old = text
    clean_text = text.lower()
    for term in search_terms_old:
        clean_text_old = clean_text_old.replace(term, '')
    for term in search_terms:
        clean_text = clean_text.replace(term, '')
    words_old = re.findall(r'\b\w+\b', clean_text_old)
    search_terms_old.extend(words_old)
    matching_files = set()
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            for term in search_terms:
                if term.lower() in file.lower():
                    term_position = search_terms.index(term)
                    matching_files.add(file)
                    matching_index.append(term_position)
                    break
    matching_files_old1 = []
    matching_index.sort()
    for x in matching_index:
        matching_files_old1.append(search_terms_origin[x])
    return matching_files, matching_files_old1

def convert_xlsx_to_csv(xlsx_file_path, csv_file_path):
    df = pd.read_excel(xlsx_file_path)
    df.to_csv(csv_file_path, index=False)

def save_list_CSV_id(file_list, id):
    text = ""
    for x in file_list:
        if x.endswith('.xlsx'):
            old = f"./user_file/{id}/{x}"
            new = old.replace(".xlsx", ".csv")
            convert_xlsx_to_csv(old, new)
            x = x.replace(".xlsx", ".csv")
        loader1 = CSVLoader(f"./user_file/{id}/{x}")
        docs1 = loader1.load()
        text += f"Dữ liệu file {x}:\n"
        for z in docs1:
            text += z.page_content + "\n"
    return text

def merge_files(file_set, file_list):
    """Hàm này ghép lại các tên file dựa trên điều kiện đã cho."""
    merged_files = {}
    for file_name in file_list:
        name = file_name.split('.')[0]
        for f in file_set:
            if name in f:
                merged_files[name] = f
                break
    return merged_files

def replace_keys_with_values(original_dict, replacement_dict):
    new_dict = {}
    for key, value in original_dict.items():
        if key in replacement_dict:
            new_key = replacement_dict[key]
            new_dict[new_key] = value
        else:
            new_dict[key] = value
    return new_dict

def aws1_csv_id(new_dict_csv, id):
    text = ""
    query_all = ""
    keyword = []
    for key, value in new_dict_csv.items():
        print(key, value)
        query_all += value
        keyword.append(key)
        test = save_list_CSV_id(keyword, id)
        text += test
    sources = ",".join(keyword)
    return text, query_all, sources

def chat_llama3(prompt_query):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Bạn là một trợ lý trung thưc, trả lời dựa trên nội dung tài liệu được cung cấp. Chỉ trả lời liên quan đến câu hỏi một cách đầy đủ chính xác, không bỏ sót thông tin."
                },
                {

                    "role": "user",
                    "content": f"{prompt_query}",
                }
            ],
            model="llama3-70b-8192",
            temperature=0.0,
            max_tokens=9000,
            stop=None,
            stream=False,
        )
        return chat_completion.choices[0].message.content
    except Exception as error:
        return False

def chat_gemini(prompt):
    generation_config = {
        "temperature": 0.0,
        "top_p": 0.0,
        "top_k": 0,
        "max_output_tokens": 8192,
    }
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]
    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)
    convo = model.start_chat(history=[])
    convo.send_message(prompt)
    return convo.last.text

def question_answer(question):
    completion = chat_llama3(question)
    if completion:
        return completion
    else:
        answer = chat_gemini(question)
        return answer

def check_persist_directory(id, file_name):
    directory_path = f"./vector_database/{id}/{file_name}"
    return os.path.exists(directory_path)

from langchain_community.vectorstores import FAISS

def check_path_exists(path):
    return os.path.exists(path)
def aws1_all_id(new_dict, text_alls, id, thread_id):
    answer = ""
    COHERE_API_KEY1 = os.getenv("COHERE_API_KEY_1")
    os.environ["COHERE_API_KEY"] = COHERE_API_KEY1
    answer_relevant = ""
    directory = ""
    for key, value in new_dict.items():
        query = value
        query = text_preprocessing(query)
        keyword, keyword2 = find_matching_files_in_docs_12_id(query, id)
        data = extract_multi_metadata_content(text_alls, keyword)
        if keyword:
            file_name = next(iter(keyword))
            text_splitter = CharacterTextSplitter(chunk_size=3200, chunk_overlap=1500)
            texts_data = text_splitter.split_text(data)

            if check_persist_directory(id, file_name):
                vectordb_query = Chroma(persist_directory=f"./vector_database/{id}/{file_name}", embedding_function=embeddings)
            else:
                vectordb_query = Chroma.from_texts(texts_data,
                                                   embedding=embeddings,
                                                   persist_directory=f"./vector_database/{id}/{file_name}")

            k_1 = len(texts_data)
            retriever = vectordb_query.as_retriever(search_kwargs={f"k": k_1})
            bm25_retriever = BM25Retriever.from_texts(texts_data)
            bm25_retriever.k = k_1
            ensemble_retriever = EnsembleRetriever(retrievers=[bm25_retriever, retriever],
                                                   weights=[0.6, 0.4])
            docs = ensemble_retriever.get_relevant_documents(f"{query}")

            path = f"./vector_database/FAISS/{id}/{file_name}"
            if check_path_exists(path):
                docsearch = FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
            else:
                docsearch = FAISS.from_documents(docs, embeddings)
                docsearch.save_local(f"./vector_database/FAISS/{id}/{file_name}")
                docsearch = FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)

            k_2 = len(docs)
            compressor = CohereRerank(top_n=3)
            retrieve3 = docsearch.as_retriever(search_kwargs={f"k": k_2})
            compression_retriever = ContextualCompressionRetriever(
                base_compressor=compressor, base_retriever=retrieve3
            )
            compressed_docs = compression_retriever.get_relevant_documents(f"{query}")

            if compressed_docs:
                data = compressed_docs[0].page_content
                text = ''.join(map(lambda x: x.page_content, compressed_docs))
                prompt_document = f"Dựa vào nội dung sau:{text}. Hãy trả lời câu hỏi sau đây: {query}. Mà không thay đổi nội dung mà mình đã cung cấp. Cuối cùng nếu câu hỏi sử dụng tiếng Việt thì phải trả lời bằng Vietnamese. Nếu câu hỏi sử dụng tiếng Anh phải trả lời bằng English"
                answer_for = question_answer(prompt_document)
                answer += answer_for + "\n"
                answer_relevant = data
                directory = file_name

    return answer, answer_relevant, directory


def extract_content_between_keywords(query, keywords):
    contents = {}
    num_keywords = len(keywords)
    keyword_positions = []
    for i in range(num_keywords):
        keyword = keywords[i]
        keyword_position = query.find(keyword)
        keyword_positions.append(keyword_position)
        if keyword_position == -1:
            continue
        next_keyword_position = len(query)
        for j in range(i + 1, num_keywords):
            next_keyword = keywords[j]
            next_keyword_position = query.find(next_keyword)
            if next_keyword_position != -1:
                break
        if i == 0:
            content_before = query[:keyword_position].strip()
        else:
            content_before = query[keyword_positions[i - 1] + len(keywords[i - 1]):keyword_position].strip()
        if i == num_keywords - 1:
            content_after = query[keyword_position + len(keyword):].strip()
        else:
            content_after = query[keyword_position + len(keyword):next_keyword_position].strip()
        content = f"{content_before} {keyword} {content_after}"
        contents[keyword] = content
    return contents

def generate_random_questions(filtered_ques_list):
    if len(filtered_ques_list) >= 2:
        random_questions = random.sample(filtered_ques_list, 2)
    else:
        random_questions = filtered_ques_list
    return random_questions

def generate_question_main(loader, name_file):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=4500, chunk_overlap=2500)
    texts = text_splitter.split_documents(loader)
    question_gen = f"nội dung {name_file} : \n"
    question_gen += texts[0].page_content
    splitter_ques_gen = RecursiveCharacterTextSplitter(
        chunk_size=4500,
        chunk_overlap=2200
    )
    chunks_ques_gen = splitter_ques_gen.split_text(question_gen)
    document_ques_gen = [Document(page_content=t) for t in chunks_ques_gen]
    llm_ques_gen_pipeline = llm
    prompt_template_vn = """
    Bạn là một chuyên gia tạo câu hỏi dựa trên tài liệu và tài liệu hướng dẫn.
    Bạn làm điều này bằng cách đặt các câu hỏi về đoạn văn bản dưới đây:

    ------------
    {text}
    ------------

    Hãy tạo ra các câu hỏi từ đoạn văn bản này.Nếu đoạn văn là tiếng Việt hãy tạo câu hỏi tiếng Việt. Nếu đoạn văn là tiếng Anh hãy tạo câu hỏi tiếng Anh.
    Hãy chắc chắn không bỏ sót bất kỳ thông tin quan trọng nào. Và chỉ tạo với đoạn tài liệu đó tối đa 5 câu hỏi liên quan tới tài liệu cung cấp nhất.Nếu trong đoạn tài liệu có các tên liên quan đến file như demo1.pdf( nhiều file khác) thì phải kèm nó vào nội dung câu hỏi bạn tạo ra.

    CÁC CÂU HỎI:
    """

    PROMPT_QUESTIONS_VN = PromptTemplate(template=prompt_template_vn, input_variables=["text"])
    refine_template_vn = ("""
    Bạn là một chuyên gia tạo câu hỏi thực hành dựa trên tài liệu và tài liệu hướng dẫn.
    Mục tiêu của bạn là giúp người học chuẩn bị cho một kỳ thi.
    Chúng tôi đã nhận được một số câu hỏi thực hành ở mức độ nào đó: {existing_answer}.
    Chúng tôi có thể tinh chỉnh các câu hỏi hiện có hoặc thêm câu hỏi mới
    (chỉ khi cần thiết) với một số ngữ cảnh bổ sung dưới đây.
    ------------
    {text}
    ------------

    Dựa trên ngữ cảnh mới, hãy tinh chỉnh các câu hỏi bằng tiếng Việt nếu đoạn văn đó cung cấp tiếng Việt. Nếu không hãy tinh chỉnh câu hỏi bằng tiếng Anh nếu đoạn đó cung cấp tiếng Anh.
    Nếu ngữ cảnh không hữu ích, vui lòng cung cấp các câu hỏi gốc. Và chỉ tạo với đoạn tài liệu đó tối đa 5 câu hỏi liên quan tới tài liệu cung cấp nhất. Nếu trong đoạn tài liệu có các tên file thì phải kèm nó vào câu hỏi.
    CÁC CÂU HỎI:
    """
                          )

    REFINE_PROMPT_QUESTIONS = PromptTemplate(
        input_variables=["existing_answer", "text"],
        template=refine_template_vn,
    )
    ques_gen_chain = load_summarize_chain(llm=llm_ques_gen_pipeline,
                                          chain_type="refine",
                                          verbose=True,
                                          question_prompt=PROMPT_QUESTIONS_VN,
                                          refine_prompt=REFINE_PROMPT_QUESTIONS)
    ques = ques_gen_chain.run(document_ques_gen)
    ques_list = ques.split("\n")
    filtered_ques_list = ["{}: {}".format(name_file, re.sub(r'^\d+\.\s*', '', element)) for element in ques_list if
                          element.endswith('?') or element.endswith('.')]
    return generate_random_questions(filtered_ques_list)

def load_file(loader):
    return loader.load()

def extract_data2(id):
    documents = []
    directory_path = f"./user_file/{id}"
    if not os.path.exists(directory_path) or not any(
            os.path.isfile(os.path.join(directory_path, f)) for f in os.listdir(directory_path)):
        return False
    tasks = []
    with ThreadPoolExecutor() as executor:
        for file in os.listdir(directory_path):
            if file.endswith(".pdf"):
                pdf_path = os.path.join(directory_path, file)
                loader = UnstructuredPDFLoader(pdf_path)
                tasks.append(executor.submit(load_file, loader))
            elif file.endswith('.docx') or file.endswith('.doc'):
                doc_path = os.path.join(directory_path, file)
                loader = Docx2txtLoader(doc_path)
                tasks.append(executor.submit(load_file, loader))
            elif file.endswith('.txt'):
                txt_path = os.path.join(directory_path, file)
                loader = TextLoader(txt_path, encoding="utf8")
                tasks.append(executor.submit(load_file, loader))
            elif file.endswith('.pptx'):
                ppt_path = os.path.join(directory_path, file)
                loader = UnstructuredPowerPointLoader(ppt_path)
                tasks.append(executor.submit(load_file, loader))
            elif file.endswith('.csv'):
                csv_path = os.path.join(directory_path, file)
                loader = UnstructuredCSVLoader(csv_path)
                tasks.append(executor.submit(load_file, loader))
            elif file.endswith('.xlsx'):
                excel_path = os.path.join(directory_path, file)
                loader = UnstructuredExcelLoader(excel_path)
                tasks.append(executor.submit(load_file, loader))
            elif file.endswith('.json'):
                json_path = os.path.join(directory_path, file)
                loader = TextLoader(json_path)
                tasks.append(executor.submit(load_file, loader))
            elif file.endswith('.md'):
                md_path = os.path.join(directory_path, file)
                loader = UnstructuredMarkdownLoader(md_path)
                tasks.append(executor.submit(load_file, loader))
        for future in as_completed(tasks):
            result = future.result()
            documents.extend(result)
    text_splitter = CharacterTextSplitter(chunk_size=4500, chunk_overlap=2500
                                          )
    texts = text_splitter.split_documents(documents)
    Chroma.from_documents(documents=texts,
                          embedding=embeddings,
                          persist_directory=f"./vector_database/{id}")
    return texts

def generate_question(id):
    directory_path = f"./user_file/{id}"
    if not os.path.exists(directory_path) or not any(
            os.path.isfile(os.path.join(directory_path, f)) for f in os.listdir(directory_path)):
        return False
    all_questions = []
    tasks = []
    with ThreadPoolExecutor() as executor:
        for file in os.listdir(directory_path):
            if file.endswith(".pdf"):
                pdf_path = os.path.join(directory_path, file)
                loader = UnstructuredPDFLoader(pdf_path).load()
                tasks.append(executor.submit(generate_question_main, loader, file))
            elif file.endswith('.docx') or file.endswith('.doc'):
                doc_path = os.path.join(directory_path, file)
                loader = Docx2txtLoader(doc_path).load()
                tasks.append(executor.submit(generate_question_main, loader, file))
            elif file.endswith('.txt'):
                txt_path = os.path.join(directory_path, file)
                loader = TextLoader(txt_path, encoding="utf8").load()
                tasks.append(executor.submit(generate_question_main, loader, file))
            elif file.endswith('.pptx'):
                ppt_path = os.path.join(directory_path, file)
                loader = UnstructuredPowerPointLoader(ppt_path).load()
                tasks.append(executor.submit(generate_question_main, loader, file))
            elif file.endswith('.json'):
                json_path = os.path.join(directory_path, file)
                loader = TextLoader(json_path, encoding="utf8").load()
                tasks.append(executor.submit(generate_question_main, loader, file))
            elif file.endswith('.md'):
                md_path = os.path.join(directory_path, file)
                loader = UnstructuredMarkdownLoader(md_path).load()
                tasks.append(executor.submit(generate_question_main, loader, file))
        for future in as_completed(tasks):
            result = future.result()
            all_questions.extend(result)
    return all_questions

class Search(BaseModel):
    queries: List[str] = Field(
        ...,
        description="Truy vấn riêng biệt để tìm kiếm, giữ nguyên ý chính câu hỏi riêng biệt",
    )

def query_analyzer(query):
    output_parser = PydanticToolsParser(tools=[Search])
    system = """Bạn có khả năng đưa ra các truy vấn tìm kiếm chính xác để lấy thông tin giúp trả lời các yêu cầu của người dùng. Các truy vấn của bạn phải chính xác, không được bỏ ngắn rút gọn.
     Nếu bạn cần tra cứu hai hoặc nhiều thông tin riêng biệt, bạn có thể làm điều đó!. Trả lời câu hỏi bằng tiếng Việt(Vietnamese), không được dùng ngôn ngữ khác"""
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "{question}"),
        ]
    )
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.0)
    structured_llm = llm.with_structured_output(Search)
    query_analyzer = {"question": RunnablePassthrough()} | prompt | structured_llm
    text = query_analyzer.invoke(query)
    return text

def handle_query(question, text_all, compression_retriever, id, thread_id):
        COHERE_API_KEY_3 = os.environ["COHERE_API_KEY_3"]
        os.environ["COHERE_API_KEY"] = COHERE_API_KEY_3
        query = question
        x = query
        keyword, key_words_old = find_matching_files_in_docs_12_id(query, id)
        # if keyword == set() or key_words_old == list():
        #     return "Not found file" 
        file_list = keyword

        if file_list:
            list_keywords2 = list(key_words_old)
            contents1 = extract_content_between_keywords(query, list_keywords2)
            merged_result = merge_files(keyword, list_keywords2)
            original_dict = contents1
            replacement_dict = merged_result
            new_dict = replace_keys_with_values(original_dict, replacement_dict)
            files_to_remove = [filename for filename in new_dict.keys() if
                               filename.endswith('.xlsx') or filename.endswith('.csv')]
            removed_files = {}
            for filename in files_to_remove:
                removed_files[filename] = new_dict[filename]
            for filename in files_to_remove:
                new_dict.pop(filename)
            test_csv = ""
            text_csv, query_csv, source = aws1_csv_id(removed_files, id)
            prompt_csv = ""
            answer_csv = ""
            if test_csv:
                prompt_csv = f"Dựa vào nội dung sau: {text_csv}. Hãy trả lời câu hỏi sau đây: {query_csv}.Bằng tiếng Việt"
                answer_csv = question_answer(prompt_csv)
            answer_document, data_relevant, source = aws1_all_id(new_dict, text_all, id, thread_id)
            answer_all1 = answer_document + answer_csv
            return answer_all1, data_relevant, source
        else:
            compressed_docs = compression_retriever.get_relevant_documents(f"{query}")
            relevance_score_float = float(compressed_docs[0].metadata['relevance_score'])
            print(relevance_score_float)
            if relevance_score_float <= 0.12:
                documents1 = []
                for file in os.listdir(f"./user_file/{id}"):
                    if file.endswith('.csv'):
                        csv_path = f"./user_file/{id}/" + file
                        loader = UnstructuredCSVLoader(csv_path)
                        documents1.extend(loader.load())
                    elif file.endswith('.xlsx'):
                        excel_path = f"./user_file/{id}/" + file
                        loader = UnstructuredExcelLoader(excel_path)
                        documents1.extend(loader.load())
                text_splitter_csv = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=2200, chunk_overlap=1500)
                texts_csv = text_splitter_csv.split_documents(documents1)
                vectordb_csv = Chroma.from_documents(documents=texts_csv,
                                                     embedding=embeddings, persist_directory=f'./vector_database/csv/{thread_id}')
                k = len(texts_csv)
                retriever_csv = vectordb_csv.as_retriever(search_kwargs={"k": k})
                llm = Cohere(temperature=0)
                compressor_csv = CohereRerank(top_n=3, model="rerank-english-v2.0")
                compression_retriever_csv = ContextualCompressionRetriever(
                    base_compressor=compressor_csv, base_retriever=retriever_csv
                )
                compressed_docs_csv = compression_retriever_csv.get_relevant_documents(f"{query}")
                file_path = compressed_docs_csv[0].metadata['source']
                print(file_path)
                if file_path.endswith('.xlsx'):
                    new = file_path.replace(".xlsx", ".csv")
                    convert_xlsx_to_csv(file_path, new)
                    loader1 = CSVLoader(new)
                else:
                    loader1 = CSVLoader(file_path)
                docs1 = loader1.load()
                text = " "
                for z in docs1:
                    text += z.page_content + "\n"
                prompt_csv = f"Dựa vào nội dung sau: {text}. Hãy trả lời câu hỏi sau đây: {query}. Bằng tiếng Việt"
                answer_csv = question_answer(prompt_csv)
                return answer_csv
            else:
                file_path = compressed_docs[0].metadata['source']
                file_path = file_path.replace('\\', '/')
                print(file_path)
                if file_path.endswith(".pdf"):
                    loader = UnstructuredPDFLoader(file_path)
                elif file_path.endswith('.docx') or file_path.endswith('doc'):
                    loader = Docx2txtLoader(file_path)
                elif file_path.endswith('.txt'):
                    loader = TextLoader(file_path, encoding="utf8")
                elif file_path.endswith('.pptx'):
                    loader = UnstructuredPowerPointLoader(file_path)
                elif file_path.endswith('.xml'):
                    loader = UnstructuredXMLLoader(file_path)
                elif file_path.endswith('.html'):
                    loader = UnstructuredHTMLLoader(file_path)
                elif file_path.endswith('.json'):
                    loader = TextLoader(file_path)
                elif file_path.endswith('.md'):
                    loader = UnstructuredMarkdownLoader(file_path)
                elif file_path.endswith('.xlsx'):
                    file_path_new = file_path.replace(".xlsx", ".csv")
                    convert_xlsx_to_csv(file_path, file_path_new)
                    loader = CSVLoader(file_path_new)
                elif file_path.endswith('.csv'):
                    loader = CSVLoader(file_path)
                text_splitter = CharacterTextSplitter(chunk_size=3200, chunk_overlap=1500)
                texts = text_splitter.split_documents(loader.load())
                k_1 = len(texts)
                file_name = os.path.basename(file_path)
                if check_persist_directory(id, file_name):
                    vectordb_file = Chroma(persist_directory=f"./vector_database/{id}/{file_name}",
                                           embedding_function=embeddings)
                else:
                    vectordb_file = Chroma.from_documents(texts,
                                                          embedding=embeddings,
                                                          persist_directory=f"./vector_database/{id}/{file_name}")
                retriever_file = vectordb_file.as_retriever(search_kwargs={f"k": k_1})
                bm25_retriever = BM25Retriever.from_documents(texts)
                bm25_retriever.k = k_1
                ensemble_retriever = EnsembleRetriever(retrievers=[bm25_retriever, retriever_file],
                                                       weights=[0.6, 0.4])
                docs = ensemble_retriever.get_relevant_documents(f"{query}")

                path = f"./vector_database/FAISS/{id}/{file_name}"
                if check_path_exists(path):
                    docsearch = FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
                else:
                    docsearch = FAISS.from_documents(docs, embeddings)
                    docsearch.save_local(f"./vector_database/FAISS/{id}/{file_name}")
                    docsearch = FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
                k_2 = len(docs)
                retrieve3 = docsearch.as_retriever(search_kwargs={f"k": k_2})
                compressor_file = CohereRerank(top_n=3, model="rerank-english-v2.0")
                compression_retriever_file = ContextualCompressionRetriever(
                    base_compressor=compressor_file, base_retriever=retrieve3
                )
                compressed_docs_file = compression_retriever_file.get_relevant_documents(f"{x}")
                query = question
                text = ''.join(map(lambda x: x.page_content, compressed_docs_file))
                prompt = f"Dựa vào nội dung sau:{text}. Hãy trả lời câu hỏi sau đây: {query}. Mà không thay đổi, chỉnh sửa nội dung mà mình đã cung cấp"
                answer = question_answer(prompt)
                list_relevant = compressed_docs_file[0].page_content
                source = file_name
                return answer, list_relevant, source
import concurrent.futures
def handle_query_upgrade_keyword_old(query_all, text_all, id,chat_history):
    COHERE_API_KEY_2 = os.environ["COHERE_API_KEY_2"]
    os.environ["COHERE_API_KEY"] = COHERE_API_KEY_2
    test = query_analyzer(query_all)
    test_string = str(test)
    matches = re.findall(r"'([^']*)'", test_string)
    vectordb = Chroma(persist_directory=f"./vector_database/{id}", embedding_function=embeddings)
    k = len(text_all)
    retriever = vectordb.as_retriever(search_kwargs={"k": k})
    compressor = CohereRerank(top_n=5, model="rerank-english-v2.0")
    compression_retriever = ContextualCompressionRetriever(base_compressor=compressor, base_retriever= retriever)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(handle_query, query, text_all, compression_retriever, id, i): query for i, query in
                   enumerate(matches)}
        results = []
        data_relevant = []
        sources = []
        for future in as_completed(futures):
            try:
                result, list_data, list_source = future.result()
                results.append(result)
                data_relevant.append(list_data)
                sources.append(list_source)
            except Exception as e:
                print(f'An error occurred: {e}')
    answer_all = ''.join(results)
    prompt1 = f"Dựa vào nội dung sau: {answer_all}. Hãy trả lời câu hỏi sau đây: {query_all}. Lưu ý rằng ngữ cảnh của cuộc trò chuyện này trước đây là: {chat_history}. Vui lòng trả lời câu hỏi mà không thay đổi, chỉnh sửa nội dung mà mình đã cung cấp."
    answer1 = question_answer(prompt1)
    return answer1, data_relevant, sources