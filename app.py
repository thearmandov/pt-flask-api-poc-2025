from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

DRUPAL_API_URL = "http://socrata-cms-poc-2024.ddev.site/jsonapi/node/wallpaper_banner"
AUTHORIZATION_HEADER = "Basic YWRtaW46cGFzc3dvcmQ="
HEADERS = {
    "Authorization": AUTHORIZATION_HEADER,
    "Content-Type": "application/vnd.api+json",
    "Accept": "application/vnd.api+json"
}

def format_payload(id, title, sort_order, image):
    return {
        "data": {
            "type": "node--wallpaper_banner",
            "id": id,
            "attributes": {
                "title": title,
                "field_sort_order": sort_order,
                "field_banner_image_link": image
            }
        }
    }

@app.route('/wallpaper_banner', methods=['GET'])
def get_wallpaper_banner():
    res = requests.get(DRUPAL_API_URL, headers = HEADERS)
    
    if res.status_code == 200:
        data = res.json().get('data', [])

        filtered_data = []
        for item in data:
            filtered_item = {
                "id": item.get("id"),
                "banner_image_link": item["attributes"].get("field_banner_image_link"),
                "font_color": item["attributes"].get("field_font_color"),
                "hero_text": item["attributes"].get("field_hero_text"),
                "title": item["attributes"].get("title"),
                "link": item["attributes"].get("field_link"),
                "shadow_color": item["attributes"].get("field_shadow_color"),
                "sort_order": item["attributes"].get("field_sort_order")
            }
            filtered_data.append(filtered_item)
    
        return jsonify(filtered_data), res.status_code
    else:
        return jsonify({"error": "Unable to fetch wallpaper banner data"}), res.status_code


@app.route('/wallpaper_banner/<id>', methods=['PATCH'])
def patch_wallpaper_banner(id):

    # When we use all of the fields, we should make sure to use: **request.json. 
    title = request.json.get('title')
    sort_order = request.json.get('sort_order')
    img = request.json.get('img')

    payload = format_payload(id, title, sort_order, img)
    
    res = requests.patch(f"{DRUPAL_API_URL}/{id}", json=payload, headers=HEADERS)
    
    if res.status_code == 200:
        return jsonify(res.json()), res.status_code
    else:
        return jsonify({"error": "Failed to update wallpaper banner"}), res.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)