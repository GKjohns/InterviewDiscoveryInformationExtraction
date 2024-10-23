TASK_ASSETS = {
    'ux_research_interview_analysis': {
        'task': '''
        Analyze the UX research interview transcript to extract the following information:
        - user_problems: list of problems or pain points mentioned by the interviewee
        - user_motivations: reasons or motivations behind the user's actions or choices
        - current_tools: existing tools or methods mentioned that the user employs
        Be thorough in your analysis and provide concise, factual insights. For the summary, focus on the key problems and needs identified. Think about the big picture and the underlying themes.
        Also, keep in mind that one person is the interviewer and the other is the interviewee. We're interested in the interviewee's experiences and perspective.
        '''.strip(),
        'json_schema': {
            "type": "object",
            "title": "ux_research_interview_analysis",
            "description": "Extract insights from a UX research interview transcript",
            "properties": {
                "user_problems": {
                    "type": "array",
                    "description": "List of problems or pain points mentioned by the interviewee",
                    "items": {
                        "type": "object",
                        "properties": {
                            "problem": {
                                "type": "string",
                                "description": "Brief description of the problem"
                            },
                            "quote": {
                                "type": "string",
                                "description": "Direct quote from the transcript that demonstrates this problem"
                            },
                            "context": {
                                "type": "string",
                                "description": "Additional context or explanation around the quote"
                            }
                        },
                        "required": ["problem", "quote", "context"]
                    }
                },
                "opportunities": {
                    "type": "array",
                    "description": "Potential solutions or improvements suggested or implied from the discussion",
                    "maxItems": 5,
                    "items": {
                        "type": "object",
                        "properties": {
                            "opportunity": {
                                "type": "string",
                                "description": "Brief description of the opportunity"
                            },
                            "quote": {
                                "type": "string",
                                "description": "Direct quote from the transcript that suggests this opportunity"
                            },
                            "potential_impact": {
                                "type": "string",
                                "description": "How this could improve the user experience"
                            }
                        },
                        "required": ["opportunity", "quote", "potential_impact"]
                    }
                },
                "user_motivations": {
                    "type": "array",
                    "description": "Reasons or motivations behind the user's actions or choices",
                    "items": {
                        "type": "object",
                        "properties": {
                            "motivation": {
                                "type": "string",
                                "description": "Description of the motivation"
                            },
                            "quote": {
                                "type": "string",
                                "description": "Direct quote from the transcript that reveals this motivation"
                            },
                            "underlying_need": {
                                "type": "string",
                                "description": "The deeper need this motivation addresses"
                            }
                        },
                        "required": ["motivation", "quote", "underlying_need"]
                    }
                },
                "current_tools": {
                    "type": "array",
                    "description": "Existing tools or methods mentioned that the user employs",
                    "items": {
                        "type": "object",
                        "properties": {
                            "tool": {
                                "type": "string",
                                "description": "Name or description of the tool"
                            },
                            "quote": {
                                "type": "string",
                                "description": "Direct quote from the transcript mentioning this tool"
                            },
                            "usage": {
                                "type": "string",
                                "description": "How the user is currently using this tool"
                            },
                            "limitations": {
                                "type": "string",
                                "description": "Any limitations or frustrations with the tool"
                            }
                        },
                        "required": ["tool", "quote", "usage", "limitations"]
                    }
                }
            },
            "required": ["user_problems", "opportunities", "user_motivations", "current_tools"]
        },
        'prompt': 'Analyze the following UX research interview transcript:\n{transcript}',
        'model': 'gpt-4o',
        'temperature': 0,
        'max_tokens': 4096
    },
    'ux_research_interview_analysis_summary': {
        'task': '''
        You are a UX research analyst tasked with writing a concise, insightful report based on a user interview transcript. Your report should focus on identifying and understanding problems, not suggesting solutions.

        Focus on:
        1. Summarizing key findings about user problems and pain points
        2. Describing the current tools and processes users employ
        3. Highlighting user needs and motivations
        4. Identifying gaps between user needs and current solutions
        5. Describing the context in which users operate

        Write the report in markdown format, ensuring your insights provide a clear picture of the current situation and challenges.
        Try to use the interviewee's own words and tone as much as possible. Try to incorporate direct quotes from the transcript (use markdown quotes or italics), BUT DO NOT INSERT QUOTES THAT ARE NOT DIRECTLY IN THE TRANSCRIPT. Use the person's name in the report.
        Provide a detailed report in markdown format, focusing on identifying problems, understanding the current situation, and highlighting user needs without suggesting solutions or next steps.
        Do not include actionable next steps, challenges, metrics, or anything that suggests a solution. The goal is to understand the current situation and identify user problems, friction, and needs.
        '''.strip(),
        'json_schema': {
            "type": "object",
            "title": "ux_research_interview_analysis_summary",
            "description": "Write a concise report focusing on problems and current situation based on a user interview transcript and extracted insights.",
            "properties": {
                "report": {
                    "type": "string",
                    "description": "The full report in markdown format"
                }
            },
            "required": ["report"]
        },
        'prompt': '''
        Based on the following UX research interview transcript, write a concise report in markdown format:
        
        Transcript:
        {transcript}
        ''',
        'model': 'gpt-4o',
        'temperature': 0.2,
        'max_tokens': 4096
    }
}
