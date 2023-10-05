import html
import re
import streamlit as st


def message_func(text, is_user=False, is_df=False):
    if is_user:
       
        message_alignment = "flex-start"
        message_bg_color = "#279EFF"
        st.markdown(
            f"""
                <div style="display: flex; align-items: center; margin-bottom: 10px; justify-content: {message_alignment};">
                    <div style="background: {message_bg_color}; color: white; border-radius: 20px; padding: 10px; margin-right: 5px; max-width: 75%; font-size: 20px;">
                        {text}\n </div>
                
                                    
               """,
            unsafe_allow_html=True,
        )
    else:
        
        message_alignment = "flex-end"
        message_bg_color = "#614BC3"

        st.markdown(
            f"""
                <div style="display: flex; align-items: center; margin-bottom: 10px; justify-content: {message_alignment};">
                        <div style="background: {message_bg_color}; color: white; border-radius: 20px; padding: 10px; margin-right: 5px; max-width: 75%; font-size: 20px;">
                        {text} \n </div>
                </div>
                """,
            unsafe_allow_html=True,
        )

