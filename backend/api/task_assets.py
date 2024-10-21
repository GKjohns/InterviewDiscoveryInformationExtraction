TASK_ASSETS = {
    'ux_research_interview_analysis': {
        'task': '''
        Analyze the UX research interview transcript to extract the following information:
        - user_problems: list of problems or pain points mentioned by the interviewee
        - user_motivations: reasons or motivations behind the user's actions or choices
        - current_tools: existing tools or methods mentioned that the user employs
        - user_needs: specific needs or requirements expressed by the user
        - success_metrics: indicators of what success looks like for the user
        - user_context: relevant background information about the user's situation
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
                            "context": {
                                "type": "string",
                                "description": "Relevant context or quote from the interview"
                            }
                        },
                        "required": ["problem", "context"]
                    }
                },
                "opportunities": {
                    "type": "array",
                    "description": "Potential solutions or improvements suggested or implied from the discussion",
                    "items": {
                        "type": "object",
                        "properties": {
                            "opportunity": {
                                "type": "string",
                                "description": "Brief description of the opportunity"
                            },
                            "potential_impact": {
                                "type": "string",
                                "description": "How this could improve the user experience"
                            }
                        },
                        "required": ["opportunity", "potential_impact"]
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
                            "underlying_need": {
                                "type": "string",
                                "description": "The deeper need this motivation addresses"
                            }
                        },
                        "required": ["motivation", "underlying_need"]
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
                            "usage": {
                                "type": "string",
                                "description": "How the user is currently using this tool"
                            },
                            "limitations": {
                                "type": "string",
                                "description": "Any limitations or frustrations with the tool"
                            }
                        },
                        "required": ["tool", "usage", "limitations"]
                    }
                },
                "user_needs": {
                    "type": "array",
                    "description": "Specific needs or requirements expressed by the user",
                    "items": {
                        "type": "object",
                        "properties": {
                            "need": {
                                "type": "string",
                                "description": "Description of the user need"
                            },
                            "importance": {
                                "type": "string",
                                "enum": ["High", "Medium", "Low"],
                                "description": "Importance level of the need"
                            },
                            "current_solution": {
                                "type": "string",
                                "description": "How this need is currently being addressed, if at all"
                            }
                        },
                        "required": ["need", "importance", "current_solution"]
                    }
                },
                "success_criteria": {
                    "type": "array",
                    "description": "Indicators of what success looks like for the user",
                    "items": {
                        "type": "object",
                        "properties": {
                            "criterion": {
                                "type": "string",
                                "description": "Description of the success criterion"
                            },
                            "evaluation": {
                                "type": "string",
                                "description": "How this criterion could be evaluated or observed"
                            }
                        },
                        "required": ["criterion", "evaluation"]
                    }
                },
                "feature_suggestions": {
                    "type": "array",
                    "description": "Specific features, functionalities, or products suggested or implied as useful",
                    "items": {
                        "type": "object",
                        "properties": {
                            "feature": {
                                "type": "string",
                                "description": "Description of the suggested feature, functionality, or product"
                            },
                            "user_benefit": {
                                "type": "string",
                                "description": "How the feature, functionality, or product would benefit the user"
                            }
                        },
                        "required": ["feature", "user_benefit"]
                    }
                },
                "analysis_summary": {
                    "type": "string",
                    "description": "A brief summary of key problems, needs, and current tools identified in the interview. Focus on factual observations without suggesting solutions."
                }
            },
            "required": ["user_problems", "opportunities", "user_motivations", "current_tools", "user_needs", "feature_suggestions", "success_criteria", "analysis_summary"]
        },
        'prompt': 'Analyze the following UX research interview transcript for a pet adoption project:\n{{content}}',
        'model': 'gpt-4o-mini',
        'temperature': 0,
        'max_tokens': 4096
    },
    'ux_research_interview_analysis_summary': {
        'task': '''
        You are a UX research analyst tasked with writing a concise, insightful report based on a user interview transcript and extracted insights for a pet adoption project. Your report should focus on identifying and understanding problems, not suggesting solutions.

        Focus on:
        1. Summarizing key findings about user problems and pain points
        2. Describing the current tools and processes users employ
        3. Highlighting user needs and motivations
        4. Identifying gaps between user needs and current solutions
        5. Describing the context in which users operate

        Write the report in markdown format, ensuring your insights provide a clear picture of the current situation and challenges in the pet adoption process.
        Try to use the interviewee's own words and tone as much as possible. Try to incorporate direct quotes from the transcript (use markdown quotes or italics). Use their name in the report.
        '''.strip(),
        'json_schema': {
            "type": "object",
            "title": "ux_research_interview_analysis_summary",
            "description": "Write a concise report focusing on problems and current situation based on a user interview transcript and extracted insights for a pet adoption project.",
            "properties": {
                "report": {
                    "type": "string",
                    "description": "The full report in markdown format"
                },
                "key_takeaway": {
                    "type": "string",
                    "description": "A single sentence summarizing the most important problem or need identified"
                }
            },
            "required": ["report", "key_takeaway"]
        },
        'prompt': '''
        Based on the following UX research interview transcript and extracted insights, write a concise report for the pet adoption project:

        Transcript:
        {{transcript}}

        Extracted Insights:
        {{extracted_insights}}

        Provide a detailed report in markdown format, focusing on identifying problems, understanding the current situation, and highlighting user needs without suggesting solutions or next steps.
        Do not include actionable next steps, challenges, metrics, or anything that suggests a solution. The goal is to understand the current situation and identify user problems, friction, and needs.
        ''',
        'model': 'gpt-4o-mini',
        'temperature': 0.2,
        'max_tokens': 4096
    }
    
}
