import json
import os
import sys
from py_common import graphql
from py_common import log

REMOVE_EXT = True


def title_from_filename(js):
    scene_id = js["id"]
    scene_title = js["title"]
    response = graphql.callGraphQL(
        """
    query FilenameBySceneId($id: ID){
      findScene(id: $id){
        files {
          path
        }
      }
    }""",
        {"id": scene_id},
    )
    assert response is not None
    path = response["findScene"]["files"][0]["path"]
    filename = os.path.basename(path)
    if REMOVE_EXT:
        filename = os.path.splitext(filename)[0]
    if scene_title != filename:
        log.info(
            f"Scene {scene_id}: Title differs from filename: '{scene_title}' => '{filename}'"
        )
        return {"title": filename}
    return {}


input = sys.stdin.read()
js = json.loads(input)

if sys.argv[1] == "title_from_filename":
    ret = title_from_filename(js)
    print(json.dumps(ret))
