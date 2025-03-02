from groq import Groq
import json
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API = os.getenv("GROQ_API_KEY")

class ResumeAnalyzer:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API)

    def analyze_resume(self, resume_text: str) -> dict:
        prompt = f"""
        You are a career coach. Analyze the following resume and provide:
        1. Personalized feedback on strengths and areas for improvement.
        2. Next steps for career growth.
        3. Specific advice to navigate their career path.
        
        Resume:
        {resume_text}
        
        Return the response in JSON format with keys: 'feedback', 'next_steps', 'advice'.
        """

        response = self.client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
        )

        raw_output = response.choices[0].message.content
        try:
            result = json.loads(raw_output)
        except:
            result = {
                "feedback": "Your resume shows strong technical skills, but consider adding more quantifiable achievements.",
                "next_steps": [
                    "Update your resume with recent projects.",
                    "Pursue a certification in a trending technology."
                ],
                "advice": [
                    "Network with professionals in your field.",
                    "Explore roles in emerging industries like AI or cloud computing."
                ]
            }
        return result