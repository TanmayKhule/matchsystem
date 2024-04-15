# matchmaking/views.py
from django.shortcuts import render
from .forms import StudentForm
from .utils import load_data_in_chunks, get_professor_recommendations_for_student_name, prepare_tfidf

# Load data
students_df = load_data_in_chunks('./Student_interests.xlsx')
professors_df = load_data_in_chunks('./Professor_interests.xlsx')

# Prepare TF-IDF and similarity matrix
tfidf_vectorizer, student_tfidf_matrix, professor_tfidf_matrix, similarity_matrix = prepare_tfidf(students_df, professors_df)


def home(request):

    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student_name = form.cleaned_data['student_name']
            threshold = form.cleaned_data.get('threshold', 0.5)
            #print(f"Student Name Received: {student_name}")
            # Check if the 'Student GUID' column exists and that the DataFrame is not empty
            if 'Student GUID' in students_df.columns and not students_df.empty:
                try:
                    recommendations = get_professor_recommendations_for_student_name(students_df, professors_df, tfidf_vectorizer, similarity_matrix, student_name, threshold)
                    return render(request, 'matchmaking/results.html', {'recommendations': recommendations})
                except KeyError:
                    # Handle the case where the 'Student GUID' is not found in the DataFrame
                    error_message = f"No student found with the GUID: {student_name}"
                    return render(request, 'matchmaking/home.html', {'form': form, 'error_message': error_message})
                    
            else:
                error_message = "The data is not loaded correctly. Please check the 'Student GUID' column in your data source."
                return render(request, 'matchmaking/home.html', {'form': form, 'error_message': error_message})
    else:
        form = StudentForm()

    return render(request, 'matchmaking/home.html', {'form': form})

# # Load your data globally or ensure it's loaded in a way that doesn't impact performance
# students_df = load_data_in_chunks('./Professor_interests.xlsx')
# professors_df = load_data_in_chunks('./Student_interests.xlsx')
# tfidf_vectorizer, student_tfidf_matrix, professor_tfidf_matrix = prepare_tfidf(students_df, professors_df)
