#!/usr/bin/env python3
"""ROS 2 文档本地预览：构建当前分支的 HTML 并启动静态 HTTP 服务。

特点：
  * 发行版名自动取自当前 git 分支（humble / jazzy），无需改脚本
  * 跳过 plugins/sphinx_adopters.py 的“外部 URL 可达性探测”
    （离线环境会 3 次重试 + 超时，非常慢；该方法在构建期临时打补丁，不改仓库文件）
  * 默认不加 -W（本地预览不该被环境性告警打断），需要严格模式时用 --strict
  * 构建完成后在本机起 http.server 提供 build/html

用法：
  /tmp/rstvenv/bin/python translate_tools/serve_local.py            # 构建 + 服务(2022)
  /tmp/rstvenv/bin/python translate_tools/serve_local.py --port 8000
  /tmp/rstvenv/bin/python translate_tools/serve_local.py --build-only
  /tmp/rstvenv/bin/python translate_tools/serve_local.py --strict    # 等价 -W，告警即错
"""
import argparse
import functools
import http.server
import os
import socket
import socketserver
import subprocess
import sys

# 仓库根目录 = 本脚本所在目录(translate_tools/)的上一级，不写死绝对路径
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'source')
OUT = os.path.join(ROOT, 'build', 'html')


def current_version():
    """发行版名 = 当前 git 分支名（humble / jazzy），取不到时退回 humble。"""
    try:
        r = subprocess.run(['git', '-C', ROOT, 'rev-parse', '--abbrev-ref', 'HEAD'],
                           capture_output=True, text=True, check=True)
        name = r.stdout.strip()
        if name and name != 'HEAD':
            return name
    except (OSError, subprocess.CalledProcessError):
        pass
    return 'humble'


def patch_url_checks():
    """让 adopters 扩展不再做外部 URL 探测（保留 YAML 结构校验）。"""
    sys.path.insert(0, ROOT)
    sys.path.insert(0, os.path.join(ROOT, 'plugins'))

    def _skip(adopters, timeout=10):
        return []

    import adopters_schema
    import sphinx_adopters

    adopters_schema.validate_adopter_urls = _skip
    sphinx_adopters.validate_adopter_urls = _skip
    print('[patch] 已禁用 adopters 外部 URL 可达性检查')


def build(strict):
    patch_url_checks()
    from sphinx.cmd.build import main as sphinx_main

    args = [
        '-b', 'html',
        '-c', ROOT,
        '-j', 'auto',
        '-D', 'smv_current_version=' + current_version(),
        SRC, OUT,
    ]
    if strict:
        args.insert(1, '-W')
    print('[build] sphinx-build ' + ' '.join(args))
    rc = sphinx_main(args)
    print('[build] exit code = %d' % rc)
    return rc


class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *a):
        sys.stderr.write('  %s\n' % (fmt % a))

    def end_headers(self):
        # 预览时禁用缓存，改完文档刷新即生效
        self.send_header('Cache-Control', 'no-store, must-revalidate')
        super().end_headers()


def pick_port(preferred):
    for port in range(preferred, preferred + 20):
        with socket.socket() as s:
            try:
                s.bind(('127.0.0.1', port))
                return port
            except OSError:
                continue
    raise SystemExit('no free port near %d' % preferred)


def serve(port):
    os.chdir(OUT)
    handler = functools.partial(Handler, directory=OUT)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(('127.0.0.1', port), handler) as httpd:
        print('[serve] http://localhost:%d/   (Ctrl+C 停止)' % port)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\n[serve] 已停止')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--port', type=int, default=2022)
    ap.add_argument('--build-only', action='store_true')
    ap.add_argument('--serve-only', action='store_true')
    ap.add_argument('--strict', action='store_true', help='把告警当错误(-W)')
    a = ap.parse_args()

    if not a.serve_only:
        if build(a.strict) != 0:
            return 1
    if not a.build_only:
        serve(pick_port(a.port))
    return 0


if __name__ == '__main__':
    sys.exit(main())
