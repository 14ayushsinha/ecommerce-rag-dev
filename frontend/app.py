import streamlit as st
import requests

API_URL = 'http://127.0.0.1:8000/search'

st.set_page_config(
    page_title='AI Product Search',
    page_icon="🛍️",
    layout='wide'
)

st.title("🛍️ AI Product Search")

query = st.text_input(
    'Search for products',
    placeholder='e.g. Voylla necklace between 300/- and 500/-'
)

limit = st.slider(
    'Number of results',
    min_value=1,
    max_value=20,
    value=5
)

if st.button('Search'):

    if query.strip():
        with st.spinner('Searching products...'):

            response = requests.post(
                API_URL,
                json={
                    'query': query,
                    'limit': limit
                }
            )

            # st.write(response.json())
        
        if response.status_code == 200:
            
            data = response.json()

            st.success(
                f'Found {len(data['results'])} products'
            )

            for product in data['results']:

                with st.container():
                    st.subheader(product['name'])

                    col1,col2,col3=st.columns(3)

                    with col1:
                        st.write(
                            f'**Brand:** {product['brand']}'
                        )
                    
                    with col2:
                        st.write(
                            f'**Price:** {product['price']}'
                        )
                    
                    with col3:
                        st.write(
                            f'**Score:** {product['score']}'
                        )
                    
                    st.write(
                        f'**Category:** '
                        f'{product['category']} -> '
                        f'{product['subcategory']}'
                    )

                    st.divider()
    

    else:
        
        st.error(f'API Error: {response.status_code}')