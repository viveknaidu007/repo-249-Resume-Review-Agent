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
        # Use triple quotes and ensure proper escaping of curly braces in the JSON structure
        prompt = f"""
        You are a career coach. Analyze the following resume and provide detailed feedback in JSON format with the following structure:
        
        {{
            "feedback": {{
                "strengths": ["list of strengths"],
                "areas_for_improvement": ["list of areas needing improvement"]
            }},
            "next_steps": {{
                "certifications": ["list of recommended certifications"],
                "networking": ["list of networking suggestions"],
                "continuous_learning": ["list of learning recommendations"]
            }},
            "advice": {{
                "personal_branding": ["list of branding tips"],
                "career_growth": ["list of growth strategies"],
                "interview_preparation": ["list of interview tips"]
            }}
        }}
        
        Provide specific, actionable advice tailored to the resume content. If certain sections are missing from the resume, suggest general improvements relevant to typical career progression.
        
        Resume:
        {resume_text}
        
        Return the response strictly in the specified JSON format. Ensure all lists contain at least 2-3 specific suggestions even if the resume lacks detail.
        """

        try:
            response = self.client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1500,
            )

            raw_output = response.choices[0].message.content
            
            # Ensure the response is valid JSON
            result = json.loads(raw_output)
            
            # Validate the structure and fill missing parts with defaults if necessary
            required_structure = {
                "feedback": {"strengths": [], "areas_for_improvement": []},
                "next_steps": {"certifications": [], "networking": [], "continuous_learning": []},
                "advice": {"personal_branding": [], "career_growth": [], "interview_preparation": []}
            }
            
            # Merge the AI response with the required structure
            for section in required_structure:
                if section not in result:
                    result[section] = required_structure[section]
                else:
                    for subsection in required_structure[section]:
                        if subsection not in result[section]:
                            result[section][subsection] = required_structure[section][subsection]
                        # Ensure each list has at least some default content if empty
                        if not result[section][subsection]:
                            result[section][subsection] = self._get_default_content(section, subsection)

            return result

        except Exception as e:
            print(f"Error processing resume: {str(e)}")
            # Return a default structured response if anything goes wrong
            return {
                "feedback": {
                    "strengths": ["Demonstrates technical skills", "Shows consistent work history"],
                    "areas_for_improvement": ["Add quantifiable achievements", "Enhance formatting for readability"]
                },
                "next_steps": {
                    "certifications": ["Consider AWS Certified Solutions Architect", "Pursue Project Management Professional (PMP)"],
                    "networking": ["Attend industry conferences", "Join relevant LinkedIn groups"],
                    "continuous_learning": ["Take online courses on Coursera", "Read industry blogs regularly"]
                },
                "advice": {
                    "personal_branding": ["Create a professional portfolio website", "Optimize LinkedIn profile"],
                    "career_growth": ["Seek mentorship opportunities", "Apply for leadership roles"],
                    "interview_preparation": ["Practice common technical questions", "Prepare a strong personal pitch"]
                }
            }

    def _get_default_content(self, section: str, subsection: str) -> list:
        """Provide default content if AI response is missing specific sections"""
        defaults = {
            "feedback": {
                "strengths": ["Shows dedication to role", "Clear career progression"],
                "areas_for_improvement": ["Include more specific results", "Add recent skills"]
            },
            "next_steps": {
                "certifications": ["Explore industry-standard certifications", "Consider technical skill certifications"],
                "networking": ["Join professional associations", "Attend local meetups"],
                "continuous_learning": ["Subscribe to industry newsletters", "Participate in webinars"]
            },
            "advice": {
                "personal_branding": ["Develop a consistent online presence", "Share expertise on social media"],
                "career_growth": ["Set clear career goals", "Seek additional responsibilities"],
                "interview_preparation": ["Research company culture", "Prepare relevant success stories"]
            }
        }
        return defaults.get(section, {}).get(subsection, [])