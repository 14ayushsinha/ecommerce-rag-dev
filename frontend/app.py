import sys
import traceback
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import streamlit as st
import requests
import time
from session.search_context import SearchContext
from session.refinement import (is_refinement, apply_refinement)
from llm.refinement_parser import llm_refine_query
from session.followup_classifier import is_followup

API_URL = 'http://127.0.0.1:8000/search'

st.set_page_config(
    page_title='AI Product Search',
    page_icon="🛍️",
    layout='wide'
)

if 'search_context' not in st.session_state:
    st.session_state.search_context = SearchContext()

#Header
st.title("🛍️ AI Product Search")
st.caption('Hybrid Search powered by BM25 + Vector Search + Qdrant')

#Sidebar
st.sidebar.header('Search Settings')

limit = st.sidebar.slider(
    'Number of Results',
    min_value=1,
    max_value=20,
    value=5
)

sort_option = st.sidebar.selectbox(
    'Sort Results',
    (
        'Relevance',
        'Price: Low to High',
        'Price: High to Low' 
    )
)

with st.sidebar:
    st.subheader('Search Context')

    st.json(st.session_state.search_context.to_dict())

#Search Bar
query = st.text_input(
    'Search for products',
    placeholder=(
        "Examples: "
        "\n• Voylla necklace between 300/- and 500/-"
        "\n• Classmate notebook under 600"
        "\n• Comfortable cotton shorts for women"
    )
)

if st.button("🔍 search", use_container_width=True):
    
    if query.strip():

        try:
            start_time = time.time()

            context = st.session_state.search_context
            # print("\n" + "="*70)
            # print("CURRENT CONTEXT")
            # print(context.to_dict())
            # print("="*70)

            followup = is_followup(context, query)
            # print(f"Current Query : {query}")
            # print(f"Is Follow-up  : {followup}")
            # print("="*70)

            if followup:

                # print(apply_refinement)
                # print(apply_refinement.__module__)
                # print(apply_refinement.__code__.co_filename)
                result = apply_refinement(query, st.session_state.search_context)

                # print(type(result))
                # print(result)

                refined_payload, source = result

                # print(refined_payload)
                # print(source)

                if source == 'llm':

                    if refined_payload is None:

                        print("\nRegex couldn't handle refinement.")
                        print("Calling LLM refinement...")

                        refined_payload = llm_refine_query(st.session_state.search_context.to_dict(), query)
                        st.session_state.search_context.update(refined_payload)

                else:
                    st.session_state.search_context.update(refined_payload)
                
                # print("=" * 60)
                # print("Sending payload")
                # print(refined_payload)
                # print(type(refined_payload))
                # print("=" * 60)
                    
                response = requests.post(
                    API_URL,
                    json = refined_payload
                )

                # print(response.status_code)
                # print(response.text)

                data = response.json()
                parsed_query = data.get('parsed_query', {})
                st.session_state.search_context.update(parsed_query)
            
            else:
                st.session_state.search_context.reset()

                response = requests.post(
                    API_URL,
                    json={
                        'query':query,
                        'limit': limit
                    }
                )

                data = response.json()
                parsed_query = data.get('parsed_query', {})
                st.session_state.search_context.update(parsed_query)

            elapsed_time = time.time() - start_time
        
            if response.status_code == 200:
                
                data = response.json()
                results = data['results']

                #Sorting
                if sort_option == 'Price: Low to High':

                    results.sort(
                        key = lambda x: x['price']
                        if x['price'] is not None
                        else float('inf')
                    )
                
                elif sort_option == 'Price: High to Low':

                    results.sort(
                        key = lambda x: x['price']
                        if x['price'] is not None
                        else 0,
                        reverse=True
                    )
                
                st.success(
                    f'Found {len(data['results'])} products'
                    f'in {elapsed_time:.2f} seconds'
                )

                if data.get("summary"):
                    st.subheader("🤖 AI Recommendation")
                    st.info(data['summary'])

                #Product cards

                for product in results:

                    with st.container(border=True):
                        col1,col2 = st.columns([1,3])

                        with col1:
                            image_url = product.get('image')

                            if image_url:
                                st.image(image_url, width=180)
                            
                            else:
                                st.image('https://placehold.co/200x200?text=No+Image', width=180)
                        
                        with col2:
                            st.subheader(product['name'])
                            st.write(
                                f'🏷️ **Brand:** '
                                f'{product['brand']}'
                            )

                            price = product.get('price')

                            if price is not None:

                                st.write(
                                    f'💰 **Price:** '
                                    f'₹{price:,}')
                                
                            else:
                                st.write("💰 **Price:** N/A")

                            st.write(
                                f'📂 **Category:** '
                                f'{product['category']}'
                            )

                            st.write(
                                f"📌 **Subcategory:** "
                                f"{product['subcategory']}" 
                            )

                            st.caption(
                                f'Retrieved using Hybrid Search + Cross Encoder'
                            )

            else:
                st.error(
                    f'API Error: '
                    f'{response.status_code}'
                )

        except Exception:
            traceback.print_exc()
            raise

    else:
        st.warning('Please enter a search query.')