# TuneJudge

This is a web application that allows users to participate in a musical Turing test and explore data analysis of
classical and pop music features. The idea of this application is inspired by my bachelor thesis and my teacher, Frank
Trollmann.
My thesis investigates the impact of training datasets on generative Machine Learning model (LSTM) in music
generation tasks. A crucial aspect of these generative models is evaluating the quality of the output through both
objective and subjective evaluation. Due to the limited resources, the original thesis focused on objective evaluation,
omitting human judgement of the generated results. The Turing test, where testers judge whether music is computer-
generated, provides an intuitive evaluation method.

The application has two main features:
1. Playing random track clips for users to evaluate - these may be either human-made music from datasets or AI-generated
pieces from LSTM experiments
2. Showcasing statistical analysis of musical differences and similarities between classical and pop music across
various aspects

### Features
##### Musical deatures analysis dashboard
Comprehensive analysis of musical characteristics comparing classical and pop music:
- Keys and tonality analysis
- Rhythm and temporal patterns
- Pitch class and pitch range characteristics
- Pitch interval analysis
- Musical complexity metrics

##### Musical Turing test
Based on the definition of Turing test, in this feature, users can:
- Listen to music tracks and guess whether they were created by AI or humans
- Rate tracks on a scale from 1 (Definitely AI) to 5 (Definitely human)

### Data Sources & Dependencies
This project relies on specialized datasets that include:
- Musical feature analysis conducted using:
  - [MATLAB's MIDI Toolbox](https://github.com/miditoolbox/1.1)
  - [MGEval](https://github.com/RichardYang40148/mgeval)
  - [Muspy](https://github.com/salu133445/muspy)
- Music datasets:
  - [MAESTRO v2.0.0 MIDI dataset](https://magenta.tensorflow.org/datasets/maestro#v200)
  - [POP909 dataset](https://github.com/music-x-lab/POP909-Dataset) 
- AI-generated music samples created through specific training approaches
- Complex musical metrics including:
  - Normalized Pairwise Variability Index(nPVI)
  - Pitch class distribution
  - Pitch interval analysis
  - Complexity, originality and melodiousness(gradus) scores

⚠️Note⚠️: Due to the specialized nature of the data and analysis required, this project cannot be fully replicated
without access to the original music feature analysis.

### Technical Architecture
**Backend: Django**
- REST API with Django REST Framework handles user rating and serve musical data
- PostgreSQL database
- Google Cloud Storage integration for large audio files

**Frontend: Streamlit**
- Interactive music player
- Rating interface for the Turing test
- Data visualization dashboards
- Analysis exploration tools

**Deployment: Render**

### Live Demo
You can explore the live application at: [TuneJudge](https://tunejudge.onrender.com)

⚠️Note⚠️: It's deployed on Render free tier. Initial load may take 3-5 minutes due to cold starts. Please refresh as
needed.

### Installation
##### Prerequisites
- Python 3.12
- PostgreSQL
##### Environment Setup
1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies
    ```bash
    pip install -r backend/requirements.txt
    pip install -r frontend/requirements.txt
    ```
4. Create a `.env` file in the backend directory with the following variables:
    ```plaintext
    # backend/.env
    
    # Django Settings
    SECRET_KEY=your_secret_key
    DEBUG=True
    
    # Database Settings
    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    ```
##### Database Setup
1. Create PostgreSQL database:
    ```bash
    createdb -U your_db_user your_db_name
    ```
2. Run migrations:
    ```bash
    CP_TundJudge/backend$ python manage.py migrate
    ```
3. Create superuser:
    ```bash
    CP_TundJudge/backend$ python manage.py createsuperuser
    ```

### Running the Application
1. Start the backend server:
    ```bash
    CP_TundJudge/backend$ python manage.py runserver
    ```
2. Start the frontend application
    ```bash
    CP_TundJudge/frontend$ streamlit run Home.py
    ```
The application will be available at the URL that command line prompt, for example
- Frontend: http://localhost:8504
- Backend admin interface: http://localhost:8000/admin/

⚠️Note⚠️: The data can be added using admin page for try-outs, most of the fields can be left blank except for "Title" 
and "Label", the uploaded files will be stored in `backend/media/` directory. The Turing Test page can be used, since 
the Data Analysis page is mostly dependent on the musical feature data that generated from tools and libraries, it will
run into error.

### API Endpoints
**Music endpoints**
- `GET /api/music/`: List all music tracks
- `GET /api/music/<id>/`: Retrieve specific music track
- `GET /api/music/random/`: Get a random music track
**Rating endpoints**
- `GET /api/ratings/`: List all ratings
- `GET /api/ratings/<id>/`: Get rating information with a specific rating ID
- `GET /ratings/song_ratings/?song=<song_id>`: Get ratings for a specific song
- `POST /api/ratings/rate_song/`: Submit a rating for a song
**Feature analysis endpoint**
- `GET /api/feature-analysis/`: Get processed music feature data for Data Analysis page

### Testing
Run backend tests:
```bash
CP_TundJudge/backend$ python manage.py runserver
```
Run frontend tests:
```bash
CP_TundJudge/frontend$ pytest tests.py
```

### Acknowledgments
Special thanks to Frank Trollmann for thesis supervision and project inspiration.
