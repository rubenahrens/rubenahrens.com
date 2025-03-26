import os
import re
from datetime import datetime
import shutil

def extract_personal_info(content):
    """Extract personal information from LaTeX content."""
    name_match = re.search(r'\\name{(.*?)}', content)
    full_name = name_match.group(1) if name_match else "Ruben Ahrens"
    
    email = re.search(r'\\email{(.*?)}', content)
    phone = re.search(r'\\phone{(.*?)}', content)
    location = re.search(r'\\printinfo{\\faHouseUser}{(.*?)}', content)
    
    return {
        'name': full_name,
        'email': email.group(1) if email else None,
        'phone': phone.group(1) if phone else None,
        'location': location.group(1) if location else None
    }

def extract_photo(content):
    """Extract photo information from LaTeX content."""
    photo = re.search(r'\\photoL{(.*?)}{(.*?)}', content)
    photo_path = photo.group(2) if photo else None
    if photo_path and not photo_path.lower().endswith(('.jpg', '.jpeg', '.png')):
        photo_path += '.jpg'
    return photo_path

def extract_skills(content):
    """Extract skills from LaTeX content."""
    skills = []
    skills_section = re.search(r'\\cvsection{Strengths}(.*?)\\medskip', content, re.DOTALL)
    if skills_section:
        skills_text = skills_section.group(1)
        skills = re.findall(r'\\cvtag{(.*?)}', skills_text)
    return skills

def extract_experience(content):
    """Extract work experience from LaTeX content."""
    experience = []
    experience_section = re.search(r'\\cvsection{Experience}(.*?)(?:\\cvsection{|\\end{paracol})', content, re.DOTALL)
    if experience_section:
        experience_text = experience_section.group(1)
        experience_entries = re.findall(r'\\experience{(.*?)}{(.*?)}{(.*?)}{(.*?)}{(.*?)}{(.*?)}', experience_text, re.DOTALL)
        for desc, title, date, exp_location, url, company in experience_entries:
            experience.append({
                'date': date,
                'company': company,
                'title': title,
                'location': exp_location,
                'description': desc
            })
    return experience

def extract_projects(content):
    """Extract projects from LaTeX content."""
    projects = []
    projects_section = re.search(r'\\cvsection{Projects}(.*?)(?:\\cvsection{|\\end{paracol})', content, re.DOTALL)
    if projects_section:
        projects_text = projects_section.group(1)
        project_entries = re.finditer(r'\\cvevent{(.*?)}{(.*?)}{(.*?)}{(.*?)}', projects_text, re.DOTALL)
        for match in project_entries:
            content_block, title, date, links = match.groups()
            
            # Extract tags
            tags = re.findall(r'\\cvtag{(.*?)}', content_block)
            
            # Clean description
            clean_desc = re.sub(r'\\cvtag{.*?}', '', content_block)
            clean_desc = re.sub(r'\\\\', ' ', clean_desc)
            clean_desc = re.sub(r'\s+', ' ', clean_desc).strip()
            
            # Clean title and date
            clean_title = re.sub(r'\s+', ' ', title).strip()
            clean_date = re.sub(r'\s+', ' ', date).strip()
            
            # Extract links
            github = re.search(r'\\cvrepo{\\faGithub}{(.*?)}', links)
            pdf = re.search(r'\\cvrepo{\\faFilePdf}{(.*?)}', links)
            youtube = re.search(r'\\cvrepo{\\faYoutube}{(.*?)}', links)
            website = re.search(r'\\cvrepo{\\faGlobe}{(.*?)}', links)
            
            projects.append({
                'title': clean_title,
                'date': clean_date,
                'description': clean_desc,
                'github': github.group(1) if github else None,
                'pdf': pdf.group(1) if pdf else None,
                'youtube': youtube.group(1) if youtube else None,
                'website': website.group(1) if website else None,
                'tags': tags
            })
    return projects

def extract_latex_info(tex_file):
    """Extract all information from LaTeX file."""
    with open(tex_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove LaTeX comments
    content = re.sub(r'%.*$', '', content, flags=re.MULTILINE)
    
    # Extract all information
    personal_info = extract_personal_info(content)
    photo_path = extract_photo(content)
    skills = extract_skills(content)
    experience = extract_experience(content)
    # projects = extract_projects(content)  # Temporarily disabled
    
    return {
        **personal_info,
        'photo': photo_path,
        'skills': skills,
        'experience': experience,
        # 'projects': projects  # Temporarily disabled
    }

def copy_assets(info):
    return
    """Copy necessary assets to public directory."""
    # Create directories
    os.makedirs('public', exist_ok=True)
    os.makedirs('public/docs', exist_ok=True)
    
    # Copy photo
    if info['photo']:
        photo_path = os.path.join('CV_Ruben_Ahrens', info['photo'])
        if os.path.exists(photo_path):
            shutil.copy2(photo_path, 'public/profile.jpg')
        else:
            print(f"Warning: Photo file {photo_path} not found.")
    
    # Copy PDF files
    pdf_files = ['CV.pdf', 'MScThesis.pdf', 'BScThesis.pdf']
    for pdf in pdf_files:
        src = os.path.join('docs', pdf)
        if os.path.exists(src):
            shutil.copy2(src, f'public/docs/{pdf}')
        else:
            print(f"Warning: Document file {src} not found.")

def generate_skills_html(skills):
    """Generate HTML for skills section."""
    return ''.join(f'''
                    <div class="skill-item">
                        <span class="skill-name">{skill}</span>
                    </div>''' for skill in skills)

def generate_experience_html(experience):
    """Generate HTML for experience section."""
    return ''.join(f'''
                <div class="experience-item">
                    <div class="experience-date">{exp['date']}</div>
                    <div class="experience-title">{exp['title']}</div>
                    <div class="experience-company">{exp['company']}</div>
                    <div class="experience-description">{exp['description']}</div>
                </div>''' for exp in experience)

def generate_projects_html(projects):
    """Generate HTML for projects section."""
    return ''.join(f'''
                <div class="project-item">
                    <div class="project-header">
                        <h3>{project['title']}</h3>
                        <div class="project-date">{project['date']}</div>
                    </div>
                    <div class="project-description">{project['description']}</div>
                    <div class="project-tags">
                        {''.join(f'<span class="tag">{tag}</span>' for tag in project['tags'])}
                    </div>
                    <div class="project-links">
                        {f'<a href="{project["github"]}" target="_blank" class="project-link"><i class="fab fa-github"></i> GitHub</a>' if project['github'] else ''}
                        {f'<a href="{project["pdf"]}" target="_blank" class="project-link"><i class="fas fa-file-pdf"></i> PDF</a>' if project['pdf'] else ''}
                        {f'<a href="{project["youtube"]}" target="_blank" class="project-link"><i class="fab fa-youtube"></i> Video</a>' if project['youtube'] else ''}
                        {f'<a href="{project["website"]}" target="_blank" class="project-link"><i class="fas fa-globe"></i> Website</a>' if project['website'] else ''}
                    </div>
                </div>''' for project in projects)

def generate_contact_html(personal_info, privacy=True):
    """Generate HTML for contact information."""
    contact_html = '''
        <a href="https://www.linkedin.com/in/ruben-ahrens/" target="_blank"><i class="fab fa-linkedin"></i> LinkedIn</a>
        <a href="https://github.com/rubenahrens" target="_blank"><i class="fab fa-github"></i> GitHub</a>
        '''
    
    # Add email if available
    if personal_info.get('email'):
        contact_html += f'''
        <a href="mailto:{personal_info['email']}"><i class="fas fa-envelope"></i> {personal_info['email']}</a>
        '''
    
    # Add phone if available
    if personal_info.get('phone') and privacy == False:
        contact_html += f'''
        <a href="tel:{personal_info['phone']}"><i class="fas fa-phone"></i> {personal_info['phone']}</a>
        '''
    
    # Add location if available
    if personal_info.get('location'):
        contact_html += f'''
        <span><i class="fas fa-map-marker-alt"></i> {personal_info['location']}</span>
        '''
    
    return contact_html

def generate_photo_html(has_photo):
    """Generate HTML for profile photo."""
    if not has_photo:
        return ''
    return '''
            <div class="profile-photo">
                <img src="profile.jpg" alt="Profile Photo">
            </div>'''

def generate_documents_html():
    """Generate HTML for documents section."""
    return '''
            <div class="card">
                <h2>Documents</h2>
                <div class="documents">
                    <a href="docs/CV.pdf" class="document-link">
                        <i class="fas fa-file-alt"></i> Curriculum Vitae
                    </a>
                    <a href="docs/MScThesis.pdf" class="document-link">
                        <i class="fas fa-graduation-cap"></i> MSc Thesis
                    </a>
                    <a href="docs/BScThesis.pdf" class="document-link">
                        <i class="fas fa-graduation-cap"></i> BSc Thesis
                    </a>
                </div>
            </div>'''

def generate_css():
    """Generate CSS styles for the page."""
    return '''
        :root {
            --primary-color: #001F5A;
            --secondary-color: #0039AC;
            --accent-color: #F3890B;
            --text-color: #2E2E2E;
            --background-color: #E2E2E2;
        }

        body {
            font-family: 'Lato', sans-serif;
            margin: 0;
            padding: 0;
            background-color: var(--background-color);
            color: var(--text-color);
            line-height: 1.6;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }

        header {
            text-align: center;
            padding: 4rem 0;
            background-color: var(--primary-color);
            color: white;
            position: relative;
        }

        .profile-photo {
            margin: 2rem auto;
            width: 200px;
            height: 200px;
            border-radius: 50%;
            overflow: hidden;
            border: 4px solid white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }

        .profile-photo img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        h1 {
            font-size: 3rem;
            margin: 0;
        }
        
        h2 {
            color: var(--primary-color);
            margin-top: 0;
            border-bottom: 2px solid var(--accent-color);
            padding-bottom: 0.5rem;
        }

        .subtitle {
            font-size: 1.5rem;
            margin-top: 1rem;
            color: var(--accent-color);
        }

        .contact-info {
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-top: 1rem;
            flex-wrap: wrap;
        }

        .contact-info a {
            color: white;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .contact-info a:hover {
            color: var(--accent-color);
        }

        .content-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }

        .card {
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            padding: 2rem;
        }

        .wide-card {
            grid-column: 1 / -1;
        }

        .skills-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
        }

        .skill-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.5rem;
            background: var(--background-color);
            border-radius: 4px;
        }

        .skill-name {
            font-weight: bold;
        }

        .experience-item {
            margin-bottom: 1.5rem;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid var(--background-color);
        }

        .experience-item:last-child {
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }

        .experience-date {
            color: var(--accent-color);
            font-weight: bold;
        }

        .experience-title {
            color: var(--primary-color);
            font-weight: bold;
            margin: 0.5rem 0;
        }

        .experience-company {
            color: var(--secondary-color);
            margin-bottom: 0.5rem;
        }
        
        .experience-description {
            margin-top: 0.5rem;
        }

        .project-item {
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--background-color);
        }
        
        .project-item:last-child {
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }
        
        .project-header {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 0.5rem;
        }
        
        .project-title {
            color: var(--primary-color);
            font-weight: bold;
            font-size: 1.2rem;
        }
        
        .project-date {
            color: var(--accent-color);
            font-weight: bold;
        }
        
        .project-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-bottom: 0.5rem;
        }
        
        .project-tag {
            background: var(--secondary-color);
            color: white;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
        }
        
        .project-description {
            margin-bottom: 0.5rem;
        }
        
        .project-links {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
        }
        
        .project-link {
            display: inline-block;
            padding: 0.3rem 0.6rem;
            background: var(--primary-color);
            color: white;
            text-decoration: none;
            border-radius: 4px;
            transition: background-color 0.3s;
        }
        
        .project-link:hover {
            background: var(--secondary-color);
        }

        .documents {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }

        .document-link {
            display: block;
            padding: 1rem;
            background: var(--primary-color);
            color: white;
            text-decoration: none;
            border-radius: 4px;
            text-align: center;
            transition: background-color 0.3s;
        }

        .document-link:hover {
            background: var(--secondary-color);
        }

        .document-link i {
            margin-right: 0.5rem;
        }

        /* Add styles for LaTeX rendering */
        .katex-display {
            margin: 1em 0;
            overflow-x: auto;
            overflow-y: hidden;
        }
        
        .katex {
            font-size: 1.1em;
        }'''

def generate_head_section(info):
    """Generate HTML head section with meta tags and styles."""
    return f'''<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{info['name']} - Portfolio</title>
    <!-- Place these in the <head> section of your index.html file -->
    <!-- SVG favicon (modern browsers) -->
    <link rel="icon" type="image/svg+xml" href="images/green-chilli-pepper-icon.svg">

    <!-- ICO favicon (traditional, works in all browsers) -->
    <link rel="shortcut icon" href="images/green-chilli-pepper-icon.ico">

    <!-- PNG favicon (alternative) -->
    <link rel="icon" type="image/png" href="images/green-chilli-pepper-icon.png"> 
    <style>
        {generate_css()}
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <!-- Add KaTeX CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
    <!-- Add KaTeX JS -->
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
</head>'''

def generate_header_section(info):
    """Generate HTML header section with photo and contact info."""
    return f'''    <header>
        <div class="container">
            {generate_photo_html(bool(info['photo']))}
            <h1>{info['name']}</h1>
            <div class="contact-info">
                {generate_contact_html(info)}
            </div>
        </div>
    </header>'''

def generate_main_section(info, skills_html, experience_html, projects_html):
    """Generate HTML main section with content grid."""
    return f'''    <main class="container">
        <div class="content-grid">
            <div class="card">
                <h2>Skills</h2>
                <div class="skills-grid">
                    {skills_html}
                </div>
            </div>

            <div class="card">
                <h2>Experience</h2>
                {experience_html}
            </div>
            
            {generate_documents_html()}

            <!-- Temporarily disabled projects section
            <div class="card wide-card">
                <h2>Projects</h2>
                {projects_html}
            </div>
            -->
        </div>
    </main>'''

def generate_scripts():
    """Generate HTML scripts section."""
    return '''    <!-- Add script to render LaTeX -->
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            renderMathInElement(document.body, {
                delimiters: [
                    {left: "$$", right: "$$", display: true},
                    {left: "$", right: "$", display: false}
                ]
            });
        });
    </script>'''

def generate_html(info):
    """Generate the complete HTML page."""
    # Generate HTML sections
    skills_html = generate_skills_html(info['skills'])
    experience_html = generate_experience_html(info['experience'])
    # projects_html = generate_projects_html(info['projects'])  # Temporarily disabled
    
    # Combine all sections
    # TODO: include projects
    html = f'''{generate_head_section(info)}
    {generate_header_section(info)}
    {generate_main_section(info, skills_html, experience_html, '')}
    {generate_scripts()}
    </body>
    </html>'''
    
    return html

def main():
    """Main function to generate the website."""
    # Extract information from LaTeX file
    info = extract_latex_info('CV_Ruben_Ahrens/main.tex')
    
    # Copy assets to public directory
    copy_assets(info)
    
    # Generate HTML
    html = generate_html(info)
    
    # Write to index.html in public directory
    with open('public/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("Website generated successfully!")

if __name__ == '__main__':
    main()