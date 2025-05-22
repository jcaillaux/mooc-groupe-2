import json
from langdetect import detect
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

sid_obj = SentimentIntensityAnalyzer()

def toxicity(text:str):
    sentiment_dict = sid_obj.polarity_scores(text)
    if sentiment_dict['compound'] >= 0.05:
        return "✅"
    elif sentiment_dict['compound'] <= -0.05:
        return "❌"
    else:
        return "⚫"


def clean_mooc_thread(thread_data, analyse=False):
    """
    Clean a FUN MOOC thread object, keeping the hierarchical structure
    but only username, body, and responses fields.
    Merges children + endorsed_responses + non_endorsed_responses into 'responses'.
    """
    
    def clean_post(post, analyze=analyse):
        global sig_obj
        """Recursively clean a post and its responses"""
        if not post:
            return None
        ppost = post
        if 'content' in post:
            ppost = post['content']
        # Extract basic fields
        cleaned = {
            'username': ppost.get('username', 'unknown'),
            'body': ppost.get('body', '') 
        }
        if analyse : 
            cleaned['lang'] = detect(cleaned['body']).upper()
            cleaned['sent'] = toxicity(cleaned['body'])
        
        # Collect all types of responses
        all_responses = []
        
        # Add children
        if 'children' in ppost.keys() and len(ppost['children']) > 0:
            all_responses.extend(ppost['children'])
        
        # Add endorsed responses
        if 'endorsed_responses' in ppost.keys() and len(ppost['endorsed_responses'])>0:
            all_responses.extend(ppost['endorsed_responses'])
        
        # Add non-endorsed responses
        if 'non_endorsed_responses' in ppost.keys() and len(ppost['non_endorsed_responses']) >0:
            all_responses.extend(ppost['non_endorsed_responses'])

        # Recursively clean all responses
        if len(all_responses) > 0:
            cleaned_responses = []
            for response in all_responses:
                cleaned_response = clean_post(response)
                if cleaned_response:  # Only add if not None/empty
                    cleaned_responses.append(cleaned_response)
            
            if cleaned_responses:  # Only add responses field if there are responses
                cleaned['responses'] = cleaned_responses
        return cleaned
    clean_thread = clean_post(thread_data)
    clean_thread['course_id'] = thread_data['content'].get('course_id', '')
    clean_thread['title'] = thread_data['content'].get('title', '')
    
    return clean_thread

if __name__ == '__main__':
    with open('../../data/G2.forum_original.json', 'r') as f:
        data = json.load(f)
    #print(data['content'])
    print(clean_mooc_thread(data))