#!/usr/bin/env python3
"""Build the network-independent Pages demo from the production evidence engine."""
from pathlib import Path
import argparse, hashlib, json, shutil, sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from core.engine import analyze, ask
from core.validation import validate_dataset
QUESTIONS = {
    'selection': '为什么选择这个回合？',
    'xfg': 'Shot xFG 是什么意思？',
    'gravity': 'Gravity 是什么意思？',
    'leverage': '回合胜率机会差是什么意思？',
    'compare': '比较全部回合的 xFG、Gravity、回合胜率机会差',
    'causal': 'Gravity 能证明牵制导致命中吗？',
    'sources': '列出这个回合的证据',
}
def build(output, presentation=None, repo='dingyucanada/courtlens'):
    if Path(output).is_symlink():
        raise ValueError('Publication output must not be a symbolic link')
    output = Path(output).resolve()
    if output == ROOT or ROOT in output.parents and output.name not in ('site-dist','dist'):
        raise ValueError('Use a separate site-dist or dist directory')
    # Fail closed rather than deleting or accidentally deploying unrelated files.
    allowed_files = {'index.html','styles.css','app.js','logic.mjs','favicon.svg',
        'data/analysis.json','data/demo.json','media/demo.mp4',
        'media/narrated-demo.mp4','media/annotated-demo.vtt',
        'presentation.pptx','.nojekyll','manifest.json'}
    if output.exists():
        for entry in output.rglob('*'):
            relative = entry.relative_to(output).as_posix()
            if entry.is_symlink() or (entry.is_dir() and relative not in {'data','media'}) or (entry.is_file() and relative not in allowed_files):
                raise ValueError(f'Unexpected publication output entry: {relative}; choose a clean directory')
    output.mkdir(parents=True, exist_ok=True)
    for name in ('index.html','styles.css','app.js','logic.mjs','favicon.svg'):
        shutil.copy2(ROOT/'site'/name, output/name)
    data_dir, media_dir = output/'data', output/'media'
    data_dir.mkdir(exist_ok=True); media_dir.mkdir(exist_ok=True)
    dataset = validate_dataset(json.loads((ROOT/'data/demo.json').read_text()))
    if dataset['provenance']['kind'] != 'synthetic':
        raise ValueError('The public rehearsal site accepts only its synthetic fixture')
    if len(dataset['possessions']) != 3 or dataset['video']['duration'] != 36:
        raise ValueError('Public demo copy expects the reviewed 3-possession, 36-second fixture')
    raw_media = ROOT/'media/demo.mp4'
    digest = hashlib.sha256(raw_media.read_bytes()).hexdigest()
    if digest != dataset['video']['sha256']:
        raise ValueError('Demo video and input digest differ; refusing unpaired public demo')
    analyses = {mode: analyze(dataset, mode) for mode in ('fan','analyst')}
    if any(sum(len(p['cues']) for p in analysis['possessions']) != 12 for analysis in analyses.values()):
        raise ValueError('Public demo copy expects 12 timed commentary cues')
    answers = {mode: {p['id']: {key: ask(dataset, q, p['id'], mode) for key,q in QUESTIONS.items()} for p in dataset['possessions']} for mode in analyses}
    # Relative URL is essential for project Pages under /<repository>/.
    dataset['video']['url'] = 'media/demo.mp4'
    bundle = {'schema_version':1, 'dataset':dataset, 'analyses':analyses, 'questions':QUESTIONS, 'answers':answers,
        'publication': {'repository':f'https://github.com/{repo}', 'mode':'static-evidence-demo', 'media_sha256':digest,
            'analysis_source':'core.engine.analyze / core.engine.ask', 'presentation_available':bool(presentation)}}
    (data_dir/'analysis.json').write_text(json.dumps(bundle,ensure_ascii=False,separators=(',',':'))+'\n')
    (data_dir/'demo.json').write_text(json.dumps(dataset,ensure_ascii=False,indent=2)+'\n')
    for name in ('demo.mp4','narrated-demo.mp4','annotated-demo.vtt'):
        shutil.copy2(ROOT/'media'/name, media_dir/name)
    if presentation:
        p=Path(presentation)
        if not p.is_file(): raise FileNotFoundError(p)
        shutil.copy2(p,output/'presentation.pptx')
    elif (output/'presentation.pptx').exists():
        (output/'presentation.pptx').unlink()
    (output/'.nojekyll').touch()
    manifest={str(p.relative_to(output)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(output.rglob('*')) if p.is_file() and p.name!='manifest.json'}
    (output/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    return bundle
if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--output',default=str(ROOT.parent/'site-dist')); parser.add_argument('--presentation'); parser.add_argument('--repo',default='dingyucanada/courtlens')
    args=parser.parse_args(); result=build(args.output,args.presentation,args.repo)
    print(json.dumps({'output':str(Path(args.output).resolve()),'possessions':len(result['dataset']['possessions']),'modes':list(result['analyses']),'questions_per_possession':len(QUESTIONS),'media_sha256':result['publication']['media_sha256']},ensure_ascii=False))
