#!/usr/bin/env python3
"""
Convert nutrition CSV data to JSON format for backend consumption
"""
import csv
import json
from pathlib import Path


def convert_csv_to_json(csv_path, json_path):
    """
    Convert nutrition CSV to structured JSON
    
    Args:
        csv_path: Path to input CSV file
        json_path: Path to output JSON file
    """
    nutrition_data = {}
    
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            ingredient_name = row['nama_bahan'].lower().strip()
            
            # Convert to proper data types
            nutrition_info = {
                'nama': row['nama_bahan'],
                'kalori_kcal': float(row['kalori_kcal']),
                'protein_g': float(row['protein_g']),
                'lemak_g': float(row['lemak_g']),
                'karbohidrat_g': float(row['karbohidrat_g']),
                'serat_g': float(row['serat_g']),
                'kalsium_mg': float(row['kalsium_mg']),
                'air_g': float(row['air_g']),
                
                # Additional calculated fields
                'kalori_per_100g': float(row['kalori_kcal']),
                'kategori_kalori': get_calorie_category(float(row['kalori_kcal'])),
                'tinggi_protein': float(row['protein_g']) > 10,
                'rendah_lemak': float(row['lemak_g']) < 5,
            }
            
            nutrition_data[ingredient_name] = nutrition_info
    
    # Save to JSON
    with open(json_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(nutrition_data, jsonfile, ensure_ascii=False, indent=2)
    
    print(f"✅ Converted {len(nutrition_data)} ingredients")
    print(f"📁 CSV: {csv_path}")
    print(f"📄 JSON: {json_path}")
    
    return nutrition_data


def get_calorie_category(calories):
    """Categorize ingredients by calorie content"""
    if calories < 50:
        return "Rendah Kalori"
    elif calories < 150:
        return "Sedang Kalori"
    else:
        return "Tinggi Kalori"


def create_nutrition_summary(nutrition_data):
    """Create summary statistics"""
    summary = {
        'total_ingredients': len(nutrition_data),
        'avg_calories': sum(item['kalori_kcal'] for item in nutrition_data.values()) / len(nutrition_data),
        'high_protein_count': sum(1 for item in nutrition_data.values() if item['tinggi_protein']),
        'low_fat_count': sum(1 for item in nutrition_data.values() if item['rendah_lemak']),
        'categories': {}
    }
    
    # Count by category
    for item in nutrition_data.values():
        category = item['kategori_kalori']
        summary['categories'][category] = summary['categories'].get(category, 0) + 1
    
    return summary


if __name__ == "__main__":
    # Paths
    csv_path = Path("../dataset/dummy_gizi.csv")
    json_path = Path("../backend/data/nutrition_data.json")
    summary_path = Path("../backend/data/nutrition_summary.json")
    
    # Create output directory
    json_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert CSV to JSON
    nutrition_data = convert_csv_to_json(csv_path, json_path)
    
    # Create summary
    summary = create_nutrition_summary(nutrition_data)
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"📊 Summary: {summary_path}")
    print(f"📈 Average calories: {summary['avg_calories']:.1f} kcal")
    print(f"🥩 High protein ingredients: {summary['high_protein_count']}")
    print(f"🥬 Low fat ingredients: {summary['low_fat_count']}")