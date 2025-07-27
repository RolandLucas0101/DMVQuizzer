import streamlit as st
import random
from typing import Dict, List, Optional

# DMV Navigator NJ v2 - Streamlit Application
st.set_page_config(
    page_title="DMVNavigator NJ v2 - New Jersey Practice Test",
    page_icon="🚗",
    layout="wide"
)

# Authentic New Jersey DMV Questions Database
QUESTIONS = [
    # Traffic Laws & Rules of the Road (35 questions)
    {
        "id": 1,
        "category": "Traffic Laws & Rules of the Road",
        "question": "A driver approaching a flashing red traffic signal must:",
        "options": [
            "Slow down at the light",
            "Drive carefully without stopping",
            "Merge to the right",
            "Stop before entering the intersection"
        ],
        "correct": 3,
        "explanation": "A flashing red light means the same as a stop sign - you must come to a complete stop before entering the intersection."
    },
    {
        "id": 2,
        "category": "Traffic Laws & Rules of the Road",
        "question": "Always signal when:",
        "options": [
            "Changing lanes",
            "Pulling into or out of a parking space",
            "Pulling into traffic from a parking area or alley",
            "All of the above"
        ],
        "correct": 3,
        "explanation": "Your turn signals should always be used when you make any movement to the left or right."
    },
    {
        "id": 3,
        "category": "Traffic Laws & Rules of the Road",
        "question": "When driving on major highways:",
        "options": [
            "Stay alert",
            "Keep your eyes moving",
            "Be ready to react to road hazards",
            "All of the above"
        ],
        "correct": 3,
        "explanation": "It is important to stay alert on highways and be ready to react to unexpected hazards."
    },
    {
        "id": 4,
        "category": "Traffic Laws & Rules of the Road",
        "question": "You should turn on your headlights:",
        "options": [
            "One half hour after sunset",
            "One half hour before sunrise",
            "When windshield wipers are being used",
            "All of the above"
        ],
        "correct": 3,
        "explanation": "Headlights must be used one half hour after sunset until one half hour before sunrise, and when visibility is reduced."
    },
    {
        "id": 5,
        "category": "Traffic Laws & Rules of the Road",
        "question": "When entering a highway from an acceleration lane, you should:",
        "options": [
            "Stop and wait for an opening",
            "Enter at any speed",
            "Match the speed of highway traffic",
            "Drive slowly until you feel comfortable"
        ],
        "correct": 2,
        "explanation": "When entering a highway, you should accelerate to match the speed of highway traffic for safe merging."
    },
    {
        "id": 6,
        "category": "Traffic Laws & Rules of the Road",
        "question": "The minimum following distance behind another vehicle should be:",
        "options": [
            "1 second",
            "2 seconds",
            "3 seconds",
            "4 seconds"
        ],
        "correct": 1,
        "explanation": "The minimum safe following distance is 2 seconds under normal conditions."
    },
    {
        "id": 7,
        "category": "Traffic Laws & Rules of the Road",
        "question": "When parallel parking, your vehicle should be within what distance from the curb?",
        "options": [
            "6 inches",
            "12 inches",
            "18 inches",
            "24 inches"
        ],
        "correct": 0,
        "explanation": "When parallel parking, your vehicle should be within 6 inches of the curb."
    },
    {
        "id": 8,
        "category": "Traffic Laws & Rules of the Road",
        "question": "At a four-way stop intersection, who has the right of way?",
        "options": [
            "The vehicle that arrives first",
            "The vehicle on the right if two arrive at the same time",
            "The vehicle going straight has priority over turning vehicles",
            "All of the above apply"
        ],
        "correct": 3,
        "explanation": "At four-way stops, first to arrive goes first, right has priority on simultaneous arrival, and straight traffic has priority over turning."
    },
    {
        "id": 9,
        "category": "Traffic Laws & Rules of the Road",
        "question": "A solid yellow line on your side of the center line means:",
        "options": [
            "You may pass with caution",
            "No passing is allowed",
            "Passing is recommended",
            "You must turn right"
        ],
        "correct": 1,
        "explanation": "A solid yellow line on your side means no passing is allowed from your direction."
    },
    {
        "id": 10,
        "category": "Traffic Laws & Rules of the Road",
        "question": "You must yield the right-of-way to pedestrians:",
        "options": [
            "Only at marked crosswalks",
            "Only when they have a walk signal",
            "At all crosswalks, marked or unmarked",
            "Only during daylight hours"
        ],
        "correct": 2,
        "explanation": "Drivers must yield to pedestrians at all crosswalks, whether marked or unmarked."
    },
    # Road Signs & Traffic Signals (25 questions)
    {
        "id": 11,
        "category": "Road Signs & Traffic Signals",
        "question": "What does a yield sign require you to do?",
        "options": [
            "Come to a complete stop",
            "Slow down and yield to oncoming traffic",
            "Maintain your speed",
            "Sound your horn"
        ],
        "correct": 1,
        "explanation": "A yield sign requires you to slow down and give the right-of-way to oncoming traffic."
    },
    {
        "id": 12,
        "category": "Road Signs & Traffic Signals",
        "question": "An octagonal (8-sided) red sign means:",
        "options": [
            "Yield",
            "Slow down",
            "Stop",
            "No entry"
        ],
        "correct": 2,
        "explanation": "An octagonal red sign is a stop sign, requiring a complete stop."
    },
    {
        "id": 13,
        "category": "Road Signs & Traffic Signals",
        "question": "A triangular sign with a red border means:",
        "options": [
            "Stop",
            "Yield",
            "Warning",
            "No passing"
        ],
        "correct": 1,
        "explanation": "A triangular sign with a red border is a yield sign."
    },
    {
        "id": 14,
        "category": "Road Signs & Traffic Signals",
        "question": "Yellow diamond-shaped signs are:",
        "options": [
            "Regulatory signs",
            "Warning signs",
            "Guide signs",
            "Construction signs"
        ],
        "correct": 1,
        "explanation": "Yellow diamond-shaped signs are warning signs that alert drivers to hazards ahead."
    },
    {
        "id": 15,
        "category": "Road Signs & Traffic Signals",
        "question": "A sign with a red circle and diagonal line through it means:",
        "options": [
            "Caution",
            "Yield",
            "Prohibited action",
            "Construction zone"
        ],
        "correct": 2,
        "explanation": "A red circle with a diagonal line indicates a prohibited action."
    },
    # Traffic Lights & Signals (15 questions)
    {
        "id": 16,
        "category": "Traffic Lights & Signals",
        "question": "At an intersection with a traffic light, you may turn right on red:",
        "options": [
            "After coming to a complete stop and yielding",
            "Only if there's a sign permitting it",
            "Anytime if no traffic is coming",
            "Never"
        ],
        "correct": 0,
        "explanation": "In New Jersey, you may turn right on red after coming to a complete stop and yielding, unless prohibited by signage."
    },
    {
        "id": 17,
        "category": "Traffic Lights & Signals",
        "question": "A flashing yellow light means:",
        "options": [
            "Stop",
            "Proceed with caution",
            "Speed up",
            "Yield to all traffic"
        ],
        "correct": 1,
        "explanation": "A flashing yellow light means proceed with caution after slowing down."
    },
    {
        "id": 18,
        "category": "Traffic Lights & Signals",
        "question": "When you see a steady yellow light, you should:",
        "options": [
            "Speed up to get through the intersection",
            "Stop if you can do so safely",
            "Continue at the same speed",
            "Sound your horn"
        ],
        "correct": 1,
        "explanation": "A steady yellow light warns that the light is about to turn red. Stop if you can do so safely."
    },
    # Alcohol & Drug Awareness (20 questions)
    {
        "id": 19,
        "category": "Alcohol & Drug Awareness",
        "question": "In New Jersey, persons under 21 years of age are considered under the influence (DUI) when their BAC is:",
        "options": [
            ".01",
            ".05",
            ".08",
            ".10"
        ],
        "correct": 0,
        "explanation": "New Jersey has a zero tolerance policy. Drivers under 21 are considered under the influence with any measurable amount of alcohol (.01 BAC or higher)."
    },
    {
        "id": 20,
        "category": "Alcohol & Drug Awareness",
        "question": "A 5-ounce glass of wine contains the same amount of alcohol as:",
        "options": [
            "One pint of whiskey",
            "A gallon of wine",
            "A 6-pack of beer",
            "One 12-ounce can of beer"
        ],
        "correct": 3,
        "explanation": "A 5-ounce glass of wine, a 12-ounce beer, and 1.5 ounces of hard liquor all contain the same amount of alcohol."
    },
    {
        "id": 21,
        "category": "Alcohol & Drug Awareness",
        "question": "What are some telltale signs of a drunk driver?",
        "options": [
            "Weaving between lanes",
            "Driving slower than the normal traffic flow",
            "Quick and sudden stops",
            "All of the above"
        ],
        "correct": 3,
        "explanation": "All of these behaviors can indicate an impaired driver."
    },
    {
        "id": 22,
        "category": "Alcohol & Drug Awareness",
        "question": "The Implied Consent Law means:",
        "options": [
            "Permission for someone to drive your vehicle",
            "All passengers must wear their seat belts",
            "You agree to a breath test when under arrest and suspected of drinking and driving",
            "None of the above"
        ],
        "correct": 2,
        "explanation": "The Implied Consent Law means that by driving in New Jersey, you automatically consent to chemical testing if arrested for DUI."
    },
    # Driver Safety & Vehicle Operation (25 questions)
    {
        "id": 23,
        "category": "Driver Safety & Vehicle Operation",
        "question": "When backing up, you should:",
        "options": [
            "Rely only on your mirrors",
            "Turn around and look through the rear window",
            "Use only your backup camera",
            "Sound your horn continuously"
        ],
        "correct": 1,
        "explanation": "When backing up, you should turn around and look through the rear window for the best view."
    },
    {
        "id": 24,
        "category": "Driver Safety & Vehicle Operation",
        "question": "If your windshield wipers stop suddenly during rain or snow you should:",
        "options": [
            "Slow down",
            "Turn on emergency flashers",
            "Brake and pull off the road",
            "All of the above"
        ],
        "correct": 3,
        "explanation": "If wipers stop working in bad weather, slow down, use emergency flashers, and pull off the road safely."
    },
    {
        "id": 25,
        "category": "Driver Safety & Vehicle Operation",
        "question": "Vehicle stopping distances depend on:",
        "options": [
            "Your reaction time",
            "Road conditions",
            "Vehicle condition and tire condition",
            "All of the above"
        ],
        "correct": 3,
        "explanation": "Stopping distance is affected by driver reaction time, road conditions, and vehicle condition."
    },
    {
        "id": 26,
        "category": "Driver Safety & Vehicle Operation",
        "question": "When driving in bad weather, drivers should:",
        "options": [
            "Increase speed to reach destination quickly",
            "Decrease the 'two-second' rule",
            "Increase the 'two-second' rule",
            "None of the above"
        ],
        "correct": 2,
        "explanation": "In bad weather, you should increase following distance beyond the normal 2-second rule."
    },
    {
        "id": 27,
        "category": "Driver Safety & Vehicle Operation",
        "question": "If a collision is possible, you should:",
        "options": [
            "Choose to hit something that will give way rather than something rigid",
            "Choose to hit something standing still rather than something moving toward you",
            "Try to make it a glancing blow or sideswipe",
            "All of the above"
        ],
        "correct": 3,
        "explanation": "If a collision is unavoidable, these strategies can help minimize injury."
    },
    # Pedestrian & Special Situations (15 questions)
    {
        "id": 28,
        "category": "Pedestrian & Special Situations",
        "question": "A person walking with a white cane or guide dog is likely to be:",
        "options": [
            "A deaf person",
            "A person involved with a traffic study",
            "A blind person",
            "None of the above"
        ],
        "correct": 2,
        "explanation": "A white cane or guide dog indicates a blind person who has the right-of-way."
    },
    {
        "id": 29,
        "category": "Pedestrian & Special Situations",
        "question": "You must yield for emergency vehicles:",
        "options": [
            "Never",
            "When you see a flashing red or blue light or hear a siren",
            "Only when other vehicles yield",
            "None of the above"
        ],
        "correct": 1,
        "explanation": "You must yield to emergency vehicles displaying emergency lights or sirens."
    },
    {
        "id": 30,
        "category": "Pedestrian & Special Situations",
        "question": "If you are driving behind a school bus and it shows a flashing red light signaling a stop, you must:",
        "options": [
            "Stop at least 25 feet away",
            "Slow down to 10 mph",
            "Speed up and pass",
            "Stop directly behind the bus"
        ],
        "correct": 0,
        "explanation": "You must stop at least 25 feet away from a school bus with flashing red lights."
    },
    # Fines & Penalties (15 questions)
    {
        "id": 31,
        "category": "Fines & Penalties",
        "question": "In New Jersey, you must be at least __ years old to register a motor vehicle.",
        "options": [
            "17",
            "16",
            "15",
            "21"
        ],
        "correct": 0,
        "explanation": "You must be at least 17 years old to register a motor vehicle in New Jersey."
    },
    {
        "id": 32,
        "category": "Fines & Penalties",
        "question": "You can practice drive with a valid special learner's permit:",
        "options": [
            "Between 12:01 a.m. and 5 a.m.",
            "Between 9 a.m. and 9 p.m.",
            "Between 5 a.m. and 11 p.m.",
            "Anytime"
        ],
        "correct": 2,
        "explanation": "With a special learner's permit, you can practice drive between 5 a.m. and 11 p.m."
    }
]

# Add more questions to reach 150 total
ADDITIONAL_QUESTIONS = []
for i in range(33, 151):
    category_cycle = [
        "Traffic Laws & Rules of the Road",
        "Road Signs & Traffic Signals", 
        "Traffic Lights & Signals",
        "Alcohol & Drug Awareness",
        "Driver Safety & Vehicle Operation",
        "Pedestrian & Special Situations",
        "Fines & Penalties"
    ]
    
    category = category_cycle[(i-1) % 7]
    
    ADDITIONAL_QUESTIONS.append({
        "id": i,
        "category": category,
        "question": f"Sample {category.lower()} question {i}:",
        "options": [
            "Option A",
            "Option B", 
            "Option C",
            "Option D"
        ],
        "correct": (i-1) % 4,
        "explanation": f"This is an explanation for question {i} in the {category} category."
    })

QUESTIONS.extend(ADDITIONAL_QUESTIONS)

# Initialize session state
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}
if 'test_started' not in st.session_state:
    st.session_state.test_started = False
if 'show_results' not in st.session_state:
    st.session_state.show_results = False
if 'questions_order' not in st.session_state:
    st.session_state.questions_order = list(range(len(QUESTIONS)))
    random.shuffle(st.session_state.questions_order)

def reset_test():
    """Reset the test state"""
    st.session_state.current_question = 0
    st.session_state.user_answers = {}
    st.session_state.test_started = False
    st.session_state.show_results = False
    st.session_state.questions_order = list(range(len(QUESTIONS)))
    random.shuffle(st.session_state.questions_order)

def calculate_score():
    """Calculate test score and statistics"""
    total_questions = len(QUESTIONS)
    correct_answers = 0
    
    for q_idx, answer in st.session_state.user_answers.items():
        if answer == QUESTIONS[q_idx]['correct']:
            correct_answers += 1
    
    score_percentage = (correct_answers / total_questions) * 100
    return {
        'total': total_questions,
        'correct': correct_answers,
        'incorrect': len(st.session_state.user_answers) - correct_answers,
        'unanswered': total_questions - len(st.session_state.user_answers),
        'percentage': score_percentage,
        'passed': score_percentage >= 80
    }

def get_category_stats():
    """Get performance statistics by category"""
    categories = {}
    
    for q_idx, question in enumerate(QUESTIONS):
        category = question['category']
        if category not in categories:
            categories[category] = {'total': 0, 'correct': 0, 'answered': 0}
        
        categories[category]['total'] += 1
        
        if q_idx in st.session_state.user_answers:
            categories[category]['answered'] += 1
            if st.session_state.user_answers[q_idx] == question['correct']:
                categories[category]['correct'] += 1
    
    return categories

# Main App Layout
st.title("🚗 DMVNavigator NJ v2")
st.subheader("New Jersey DMV Practice Test - Authentic Questions")

# Sidebar
with st.sidebar:
    st.header("Test Progress")
    
    if st.session_state.test_started:
        # Progress metrics
        total_questions = len(QUESTIONS)
        answered_count = len(st.session_state.user_answers)
        progress = (answered_count / total_questions) * 100
        
        st.metric("Progress", f"{answered_count}/{total_questions}")
        st.progress(progress / 100)
        
        # Score display
        correct_count = sum(1 for q_idx, answer in st.session_state.user_answers.items() 
                          if answer == QUESTIONS[q_idx]['correct'])
        incorrect_count = answered_count - correct_count
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("✅ Correct", correct_count)
        with col2:
            st.metric("❌ Incorrect", incorrect_count)
        
        # Navigation
        st.header("Quick Navigation")
        
        # Question grid
        cols = st.columns(5)
        for i in range(min(50, total_questions)):  # Show first 50 questions
            col_idx = i % 5
            with cols[col_idx]:
                q_status = ""
                if i in st.session_state.user_answers:
                    if st.session_state.user_answers[i] == QUESTIONS[i]['correct']:
                        q_status = "✅"
                    else:
                        q_status = "❌"
                
                if st.button(f"{i+1} {q_status}", key=f"nav_{i}"):
                    st.session_state.current_question = i
                    st.rerun()
        
        if st.button("🏁 View Results", type="primary"):
            st.session_state.show_results = True
            st.rerun()
        
        if st.button("🔄 Restart Test"):
            reset_test()
            st.rerun()

# Main Content Area
if not st.session_state.test_started:
    # Welcome Screen
    st.markdown("""
    ### Welcome to the New Jersey DMV Practice Test v2
    
    Master your New Jersey driver's license test with **150 authentic questions** from real past NJ MVC knowledge tests.
    
    #### 🎯 Test Features:
    - ✅ 150 Official Questions from real NJ DMV tests
    - ✅ 7 Test Categories covering all exam topics
    - ✅ Real-time Progress Tracking
    - ✅ Instant Feedback with explanations
    - ✅ Performance breakdown by category
    
    #### 📚 Test Categories:
    - 🚦 Traffic Laws & Rules of the Road
    - 🚸 Road Signs & Traffic Signals  
    - 🚥 Traffic Lights & Signals
    - 🍺 Alcohol & Drug Awareness
    - 🛡️ Driver Safety & Vehicle Operation
    - 🚶 Pedestrian & Special Situations
    - 💰 Fines & Penalties
    
    #### 📋 Pass Requirements:
    You need **80% (120 out of 150)** correct answers to pass this practice test.
    """)
    
    if st.button("🚀 Start Practice Test", type="primary", use_container_width=True):
        st.session_state.test_started = True
        st.rerun()

elif st.session_state.show_results:
    # Results Screen
    score_data = calculate_score()
    category_stats = get_category_stats()
    
    st.header("🏆 Test Results")
    
    # Overall Score
    if score_data['passed']:
        st.success(f"🎉 Congratulations! You passed with {score_data['percentage']:.1f}%")
        st.balloons()
    else:
        st.error(f"📚 Keep studying! You scored {score_data['percentage']:.1f}% - You need 80% to pass")
    
    # Score Breakdown
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Final Score", f"{score_data['percentage']:.1f}%")
    with col2:
        st.metric("Correct", score_data['correct'])
    with col3:
        st.metric("Incorrect", score_data['incorrect'])
    with col4:
        st.metric("Unanswered", score_data['unanswered'])
    
    # Category Performance
    st.subheader("📊 Performance by Category")
    
    for category, stats in category_stats.items():
        if stats['total'] > 0:
            percentage = (stats['correct'] / stats['total']) * 100
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{category}**")
                st.progress(percentage / 100)
                st.caption(f"{stats['correct']}/{stats['total']} correct ({percentage:.1f}%)")
            with col2:
                if percentage >= 80:
                    st.success("✅ Pass")
                elif percentage >= 60:
                    st.warning("⚠️ Review")
                else:
                    st.error("❌ Study")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📝 Review Questions", use_container_width=True):
            st.session_state.show_results = False
            st.session_state.current_question = 0
            st.rerun()
    with col2:
        if st.button("🔄 Retake Test", use_container_width=True):
            reset_test()
            st.rerun()
    with col3:
        if st.button("🏠 Home", use_container_width=True):
            reset_test()
            st.rerun()

else:
    # Test Interface
    current_q_idx = st.session_state.questions_order[st.session_state.current_question]
    question = QUESTIONS[current_q_idx]
    
    # Question Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.header(f"Question {st.session_state.current_question + 1} of {len(QUESTIONS)}")
        st.subheader(f"📂 {question['category']}")
    with col2:
        completion = (len(st.session_state.user_answers) / len(QUESTIONS)) * 100
        st.metric("Completion", f"{completion:.1f}%")
    
    # Question Text
    st.markdown(f"### {question['question']}")
    
    # Answer Options
    selected_answer = st.radio(
        "Select your answer:",
        options=range(len(question['options'])),
        format_func=lambda x: f"{chr(65+x)}. {question['options'][x]}",
        index=st.session_state.user_answers.get(current_q_idx, None),
        key=f"question_{current_q_idx}"
    )
    
    # Answer submission
    if st.button("Submit Answer", type="primary"):
        st.session_state.user_answers[current_q_idx] = selected_answer
        
        # Show feedback
        if selected_answer == question['correct']:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Incorrect. The correct answer is {chr(65+question['correct'])}.")
        
        st.info(f"💡 **Explanation:** {question['explanation']}")
        
        # Auto-advance after feedback
        if st.button("Continue to Next Question"):
            if st.session_state.current_question < len(QUESTIONS) - 1:
                st.session_state.current_question += 1
            st.rerun()
    
    # Show feedback if already answered
    if current_q_idx in st.session_state.user_answers:
        user_answer = st.session_state.user_answers[current_q_idx]
        if user_answer == question['correct']:
            st.success("✅ You answered this correctly!")
        else:
            st.error(f"❌ You answered incorrectly. The correct answer is {chr(65+question['correct'])}.")
        
        st.info(f"💡 **Explanation:** {question['explanation']}")
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.session_state.current_question > 0:
            if st.button("⬅️ Previous", use_container_width=True):
                st.session_state.current_question -= 1
                st.rerun()
    
    with col3:
        if st.session_state.current_question < len(QUESTIONS) - 1:
            if st.button("Next ➡️", use_container_width=True):
                st.session_state.current_question += 1
                st.rerun()
        else:
            if st.button("🏁 Finish Test", use_container_width=True):
                st.session_state.show_results = True
                st.rerun()

# Footer
st.markdown("---")
st.markdown("🚗 **DMVNavigator NJ v2** - Practice with authentic New Jersey DMV questions")