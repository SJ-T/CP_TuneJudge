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

**Note**: Due to the specialized nature of the data and analysis required, this project cannot be fully replicated
without access to the original music feature analysis.

### Technical Architecture
**Backend: Django + Django REST Framework**
- Serves analyzed musical data
- Handles user ratings
- Manages music file storage
- Provides data analysis endpoints

**Frontend: Streamlit**
- Interactive music player
- Rating interface for the Turing test
- Data visualization dashboards
- Analysis exploration tools

**Infrastructure**
- Database: PostgresSQL
- Music Storage: Google Cloud Storage
- Deployment: Render

### Live Demo
You can explore the live application at: [TuneJudge](https://tunejudge.onrender.com)

**Note**: It's deployed on Render free tier. Initial load may take 3-5 minutes due to cold starts. Please refresh as
needed.

### Development
While the full project requires specific data dependencies, the codebase demonstrates:
- Django REST Framework implementation
- Strealit data visualization
- Goolgle Cloud Storage integration
- Frontend-backend integration patterns
- CI/CD implementation

### Acknowledgments
Special thanks to Frank Trollmann for thesis supervision and project inspiration.
