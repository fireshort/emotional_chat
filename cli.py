#!/usr/bin/env python
"""
情感聊天机器人命令行工具

统一的CLI入口，替代 Makefile
"""

import sys
import argparse
import subprocess
from pathlib import Path


def run_backend():
    """运行后端服务"""
    print("🚀 启动情感聊天机器人后端服务...")
    subprocess.run([sys.executable, "run_backend.py"], check=True)


def db_command(args):
    """数据库管理命令"""
    cmd_args = [sys.executable, "db_manager.py", args.action]
    subprocess.run(cmd_args, check=True)


def rag_command(args):
    """RAG知识库命令"""
    if args.action == "init":
        subprocess.run([sys.executable, "init_rag_knowledge.py"], check=True)
    elif args.action == "test":
        print("📝 测试RAG系统...")
        print("检查RAG API端点: http://localhost:8000/api/rag/test")
        try:
            import requests
            response = requests.get("http://localhost:8000/api/rag/test")
            print(f"✅ 状态码: {response.status_code}")
            print(response.json())
        except Exception as e:
            print(f"⚠️  请确保后端服务正在运行: {e}")
    elif args.action == "demo":
        print("🎬 演示RAG效果对比...")
        print("测试问题: 失眠怎么办？")
        try:
            import requests
            response = requests.post(
                "http://localhost:8000/api/rag/ask",
                json={"question": "失眠怎么办？"}
            )
            print(f"✅ 状态码: {response.status_code}")
            print(response.json())
        except Exception as e:
            print(f"⚠️  请确保后端服务正在运行: {e}")


def main():
    """主入口函数"""
    parser = argparse.ArgumentParser(
        description="情感聊天机器人命令行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  %(prog)s run              # 运行后端服务
  %(prog)s db upgrade       # 升级数据库
  %(prog)s db check         # 检查数据库连接
  %(prog)s rag init         # 初始化RAG知识库
  %(prog)s rag test         # 测试RAG系统
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # 运行后端服务
    subparsers.add_parser("run", help="运行后端服务")

    # 数据库管理
    db_parser = subparsers.add_parser("db", help="数据库管理命令")
    db_parser.add_argument(
        "action",
        choices=["init", "upgrade", "downgrade", "check", "current", "history", "reset"],
        help="数据库操作"
    )

    # RAG知识库
    rag_parser = subparsers.add_parser("rag", help="RAG知识库命令")
    rag_parser.add_argument(
        "action",
        choices=["init", "test", "demo"],
        help="RAG操作"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        if args.command == "run":
            run_backend()
        elif args.command == "db":
            db_command(args)
        elif args.command == "rag":
            rag_command(args)
    except KeyboardInterrupt:
        print("\n\n⚠️  操作被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
