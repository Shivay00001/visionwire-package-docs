import os
from visionwire_advanced_scraper import AdvancedScraper
from visionwire_hybrid import VisionWireHybrid
from visionwire_universal_config import HTML_TEMPLATE, DIFFICULTY_PRESETS

class UniversalStudyPackGenerator:
    def __init__(self):
        self.scraper = AdvancedScraper()
        self.hybrid = VisionWireHybrid()

    def generate_universal_pack(self, class_level, exam, subject, chapter, language='english', difficulty='balanced'):
        print(f"Generating study pack for {chapter} ({subject}, {exam}, Class {class_level})...")
        
        # 1. Scrape context
        scraped_data = self.scraper.scrape_topic(f"{subject} {chapter}")
        
        # 2. Construct Prompt
        prompt = f"""
        Generate a comprehensive study pack for:
        Class: {class_level}
        Exam: {exam}
        Subject: {subject}
        Chapter: {chapter}
        Language: {language}
        Difficulty: {difficulty}
        
        Context Data: {scraped_data}
        
        The pack should include:
        1. A 600-word summary.
        2. 10 important points.
        3. 10 MCQs with options and answers.
        """
        
        # 3. Generate content via LLM
        ai_content = self.hybrid.generate_content(prompt)
        
        # 4. Format into HTML
        html_output = HTML_TEMPLATE.format(
            class_level=class_level,
            exam=exam,
            subject=subject,
            chapter=chapter,
            content_summary=ai_content,
            important_points="<li>Point 1</li><li>Point 2</li>", # Simplified for demo
            mcqs=f"<p>{ai_content[:500]}...</p>"
        )
        
        # 5. Save output
        output_filename = f"output/{subject}_{chapter}_{language}.html"
        if not os.path.exists('output'):
            os.makedirs('output')
            
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(html_output)
            
        print(f"✅ Study pack generated: {output_filename}")
        return ai_content, output_filename

if __name__ == "__main__":
    # Example usage
    generator = UniversalStudyPackGenerator()
    generator.generate_universal_pack("12", "NEET", "Biology", "Human Reproduction", "hindi")
