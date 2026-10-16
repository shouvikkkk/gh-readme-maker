# gh-readme-maker


Generate a professional GitHub profile README from a simple JSON config. Python 3 standard library only — no dependencies.


## Usage


```sh
python readme_maker.py example.json > README.md
```


Then paste the generated markdown into the README of your `<username>/<username>` profile repository.


Show help:


```sh
python readme_maker.py --help
```


## Config format


The config is a JSON object. Only `name` is required — any section whose data is missing or empty is left out of the output, so you never get an empty "Projects" table or a blank badge row.


| Field      | Type   | Required | Description |
| ---------- | ------ | -------- | ----------- |
| `name`     | string | yes      | Your display name, shown in the centered greeting at the top. |
| `tagline`  | string | no       | One short line under your name. |
| `about`     | string | no       | One or two sentences describing what you do. Becomes the About section. |
| `projects` | array  | no       | List of `{name, url, description}` objects. Rendered as a Name \| Description table; the name links to the URL when one is given. |
| `skills`   | array  | no       | Each entry is either a plain name string — a shields.io badge is generated automatically — or a `{name, badge_url}` object to use your own badge image. |
| `socials`  | array  | no       | List of `{label, url}` objects, rendered as centered links. |


`example.json` in this repo shows every field in action.


## License


MIT — see [LICENSE](LICENSE).


## FAQ


**Does it need any dependencies?** — No, it uses only the Python standard library.


**Can I preview before writing the file?** — Yes: run `python readme_maker.py config.json` and redirect or pipe the output wherever you like.
