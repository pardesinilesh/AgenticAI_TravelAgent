#!/usr/bin/env python3
"""
Generate architecture flow diagram as PNG image.
No external dependencies - uses matplotlib and PIL
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.lines as mlines

# Create figure with high DPI for better quality
fig, ax = plt.subplots(1, 1, figsize=(16, 12), dpi=300)
ax.set_xlim(0, 16)
ax.set_ylim(0, 12)
ax.axis('off')

# Color scheme
color_input = '#E8F4F8'
color_agent = '#FFE8B6'
color_component = '#D4EDDA'
color_output = '#F0E6FF'
color_llm = '#FFE0E0'
color_google = '#E0F0FF'

# Helper function to draw boxes
def draw_box(ax, x, y, width, height, text, color, fontsize=10, fontweight='normal'):
    """Draw a fancy box with text"""
    box = FancyBboxPatch(
        (x - width/2, y - height/2), width, height,
        boxstyle="round,pad=0.1", 
        edgecolor='black', 
        facecolor=color,
        linewidth=2
    )
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize, 
            fontweight=fontweight, wrap=True)

# Helper function to draw arrows
def draw_arrow(ax, x1, y1, x2, y2, label=''):
    """Draw an arrow from (x1,y1) to (x2,y2)"""
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle='->', 
        mutation_scale=30, 
        linewidth=2.5,
        color='black'
    )
    ax.add_patch(arrow)
    if label:
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mid_x + 0.3, mid_y, label, fontsize=9, style='italic')

# Title
ax.text(8, 11.5, 'Travel Planning Agent System - Architecture Flow', 
        ha='center', va='center', fontsize=18, fontweight='bold')
ax.text(8, 11, 'LLM-Based Agents + Real Google APIs + Machine Learning', 
        ha='center', va='center', fontsize=12, style='italic', color='#333333')

# ===== LAYER 1: USER INPUT =====
draw_box(ax, 8, 10, 4, 0.6, 'USER INPUT\nDestinations, Budget, Interests, Dates', color_input, 11, 'bold')

# Arrow down
draw_arrow(ax, 8, 9.7, 8, 9.2)

# ===== LAYER 2: INTELLIGENT ORCHESTRATOR =====
draw_box(ax, 8, 8.8, 5, 0.6, 'INTELLIGENT ORCHESTRATOR\n6-Step Reasoning Chain', '#FFF8DC', 11, 'bold')

# Arrow down
draw_arrow(ax, 8, 8.5, 8, 7.8)

# ===== LAYER 3: THREE AGENTS =====
# Agent 1: Destination
draw_box(ax, 3, 7.2, 3.5, 1.2, 
         'AGENT 1\nDESTINATION\nRECOMMENDER\n\n✓ Google APIs\n✓ LLM Reasoning\n✓ Memory Learning', 
         color_agent, 9, 'bold')

# Agent 2: Itinerary
draw_box(ax, 8, 7.2, 3.5, 1.2, 
         'AGENT 2\nITINERARY\nPLANNER\n\n✓ Real Activities\n✓ Distance Routing\n✓ LLM Planning', 
         color_agent, 9, 'bold')

# Agent 3: Budget
draw_box(ax, 13, 7.2, 3.5, 1.2, 
         'AGENT 3\nBUDGET\nOPTIMIZER\n\n✓ Real Prices\n✓ LLM Optimization\n✓ Auto Health Check', 
         color_agent, 9, 'bold')

# Arrows from orchestrator to agents
draw_arrow(ax, 6.5, 8.5, 3, 7.8)
draw_arrow(ax, 8, 8.5, 8, 7.8)
draw_arrow(ax, 9.5, 8.5, 13, 7.8)

# Arrows converging down
draw_arrow(ax, 3, 6.6, 6, 6)
draw_arrow(ax, 8, 6.6, 8, 6)
draw_arrow(ax, 13, 6.6, 10, 6)

# ===== LAYER 4: AI COMPONENTS (5 showing) =====
y_components = 5.2

# Component 1: LLM
draw_box(ax, 2, y_components, 2.5, 0.8, 
         'LLM SERVICE\n(GPT-3.5/4)\n\nReasoning', 
         color_llm, 8, 'bold')

# Component 2: Memory
draw_box(ax, 5, y_components, 2.5, 0.8, 
         'MEMORY\nSYSTEM\n\nUser History', 
         color_component, 8, 'bold')

# Component 3: ML
draw_box(ax, 8, y_components, 2.5, 0.8, 
         'PERSONALIZATION\nENGINE (ML)\n\nLearning', 
         color_component, 8, 'bold')

# Component 4: Google API
draw_box(ax, 11, y_components, 2.5, 0.8, 
         'GOOGLE API\nSERVICE\n\nReal Data', 
         color_google, 8, 'bold')

# Component 5: Shows connection
draw_box(ax, 14, y_components, 2, 0.8, 
         'All 5\nIntegrated\n✓ Active', 
         '#F5F5F5', 8)

# Arrows to components
for x in [2, 5, 8, 11]:
    draw_arrow(ax, 8, 6, x, 5.6)
draw_arrow(ax, 8, 6, 14, 5.6)

# ===== LAYER 5: DECISION LOGIC =====
y_decisions = 3.8

draw_box(ax, 8, y_decisions, 6, 1,
         'AUTONOMOUS DECISIONS\n' + 
         'Pace Detection | Budget Health | Variety Check | Revision Need',
         '#FFF0F5', 9, 'bold')

# Arrows from components down
for x in [2, 5, 8, 11]:
    draw_arrow(ax, x, y_components - 0.4, 8, y_decisions + 0.5)

# ===== LAYER 6: OUTPUT =====
y_output = 2

draw_box(ax, 8, y_output, 6, 1.2,
         'FINAL TRIP PLAN WITH:\n' +
         '✓ Ranked Destinations | ✓ 14-Day Itinerary | ✓ Optimized Budget\n' +
         '✓ AI Insights | ✓ Autonomous Alerts | ✓ Learning Profile',
         color_output, 9, 'bold')

# Arrow to output
draw_arrow(ax, 8, y_decisions - 0.5, 8, y_output + 0.6)

# ===== LEGENDS & ANNOTATIONS =====
y_legend = 0.5

# Key Points
ax.text(0.5, y_legend + 0.3, '✓ Real Google APIs (Places, Distance, Geocoding)', 
        fontsize=9, fontweight='bold', color='#0066CC')
ax.text(0.5, y_legend - 0.2, '✓ LLM Reasoning (OpenAI GPT-3.5/GPT-4)', 
        fontsize=9, fontweight='bold', color='#CC0000')
ax.text(8, y_legend + 0.3, '✓ Machine Learning (Adaptive Weights)', 
        fontsize=9, fontweight='bold', color='#006600')
ax.text(8, y_legend - 0.2, '✓ User Memory (Persistent History)', 
        fontsize=9, fontweight='bold', color='#660066')
ax.text(14, y_legend + 0.3, '✓ NO Hardcoded Rules', 
        fontsize=9, fontweight='bold', color='#FF6600')
ax.text(14, y_legend - 0.2, '✓ Autonomous & Self-Improving', 
        fontsize=9, fontweight='bold', color='#FF0000')

# Save as PNG with high quality
output_file = '/Users/pardesinilesh/Downloads/AgenticAL_Travelling_Assitance/docs/architecture_flow_diagram.png'
plt.tight_layout()
plt.savefig(output_file, format='png', dpi=300, bbox_inches='tight', facecolor='white')
print(f"✓ Architecture flow diagram created: {output_file}")
print(f"  Size: 16x12 inches @ 300 DPI (High Quality)")
print(f"  Format: PNG (ready to upload)")

# Also create a JPEG version
jpeg_file = '/Users/pardesinilesh/Downloads/AgenticAL_Travelling_Assitance/docs/architecture_flow_diagram.jpg'
plt.savefig(jpeg_file, format='jpg', dpi=300, bbox_inches='tight', facecolor='white', quality=95)
print(f"✓ JPEG version also created: {jpeg_file}")

plt.close()

# Create second diagram - Component Detail
fig2, ax2 = plt.subplots(1, 1, figsize=(14, 10), dpi=300)
ax2.set_xlim(0, 14)
ax2.set_ylim(0, 10)
ax2.axis('off')

# Title
ax2.text(7, 9.5, '5 AI Components - Detailed View', 
         ha='center', va='center', fontsize=16, fontweight='bold')

components_detail = [
    {
        'x': 2.5, 'y': 7.5, 'title': '1. LLM SERVICE',
        'details': 'OpenAI GPT-3.5/GPT-4\n\n• reason_about_destinations()\n• generate_itinerary_description()\n• optimize_budget_reasoning()\n• evaluate_trip_satisfaction()\n• generate_travel_tips()\n• should_revise_plan()',
        'color': color_llm
    },
    {
        'x': 7, 'y': 7.5, 'title': '2. MEMORY SYSTEM',
        'details': 'User History & Context\n\n• User profiles\n• Trip history (JSON)\n• Favorite destinations\n• Avoided destinations\n• Learning patterns\n• Preference evolution',
        'color': color_component
    },
    {
        'x': 11.5, 'y': 7.5, 'title': '3. PERSONALIZATION',
        'details': 'Machine Learning\n\n• Dynamic weight adjustment\n• Learn from feedback\n• Predict satisfaction\n• Recommend alternatives\n• Learning rate: 0.05\n• Improves per trip',
        'color': color_component
    },
    {
        'x': 2.5, 'y': 3.8, 'title': '4. GOOGLE API SERVICE',
        'details': 'Real-World Data\n\n• Places Search API\n• Place Details API\n• Distance Matrix API\n• Geocoding API\n• Real ratings & reviews\n• Live pricing & hours',
        'color': color_google
    },
    {
        'x': 7, 'y': 3.8, 'title': '5. ORCHESTRATOR',
        'details': 'Master Coordinator\n\n• 6-step reasoning chain\n• Autonomous decisions\n• Pace detection\n• Budget health checks\n• Variety detection\n• Trip learning trigger',
        'color': '#FFF8DC'
    },
]

for comp in components_detail:
    # Draw main box
    box = FancyBboxPatch(
        (comp['x'] - 1.8, comp['y'] - 1.5), 3.6, 3,
        boxstyle="round,pad=0.15",
        edgecolor='black',
        facecolor=comp['color'],
        linewidth=2.5
    )
    ax2.add_patch(box)
    
    # Title
    ax2.text(comp['x'], comp['y'] + 1.2, comp['title'],
             ha='center', va='top', fontsize=11, fontweight='bold')
    
    # Details
    ax2.text(comp['x'], comp['y'] + 0.5, comp['details'],
             ha='center', va='center', fontsize=8, wrap=True)

# Bottom section: How they work together
ax2.text(7, 1.5, 'HOW THEY WORK TOGETHER:',
         ha='center', va='center', fontsize=12, fontweight='bold')

ax2.text(7, 0.8,
         'All 5 components work together: Google APIs provide real data → LLM reasons about it →' +
         '\nMemory stores history → ML learns from feedback → Orchestrator coordinates autonomously',
         ha='center', va='center', fontsize=9, style='italic')

# Save second diagram
png_file2 = '/Users/pardesinilesh/Downloads/AgenticAL_Travelling_Assitance/docs/components_detail_diagram.png'
plt.tight_layout()
plt.savefig(png_file2, format='png', dpi=300, bbox_inches='tight', facecolor='white')
print(f"✓ Components detail diagram created: {png_file2}")

jpg_file2 = '/Users/pardesinilesh/Downloads/AgenticAL_Travelling_Assitance/docs/components_detail_diagram.jpg'
plt.savefig(jpg_file2, format='jpg', dpi=300, bbox_inches='tight', facecolor='white', quality=95)
print(f"✓ JPEG version: {jpg_file2}")

plt.close()

print("\n" + "="*70)
print("✅ DIAGRAMS CREATED SUCCESSFULLY")
print("="*70)
print("\nPNG files (ready to upload):")
print(f"  1. {output_file}")
print(f"  2. {png_file2}")
print("\nJPEG files (alternative format):")
print(f"  1. {jpeg_file}")
print(f"  2. {jpg_file2}")
print("\nBoth formats available - choose whichever works best!")
print("="*70)
