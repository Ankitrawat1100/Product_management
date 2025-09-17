import json
import sys
import argparse
import requests

API = "http://127.0.0.1:5000/api"


def create(args):
    payload = {"name": args.name, "qty": args.qty, "price": args.price}
    r = requests.post(f"{API}/products", json=payload, timeout=10)
    print(json.dumps(r.json(), indent=2))
    r.raise_for_status()


def list_(args):
    r = requests.get(f"{API}/products", timeout=10)
    print(json.dumps(r.json(), indent=2))
    r.raise_for_status()


def get_(args):
    r = requests.get(f"{API}/products/{args.id}", timeout=10)
    print(json.dumps(r.json(), indent=2))
    r.raise_for_status()


def update(args):
    payload = {}
    if args.name is not None:
        payload["name"] = args.name
    if args.qty is not None:
        payload["qty"] = args.qty
    if args.price is not None:
        payload["price"] = args.price
    r = requests.patch(f"{API}/products/{args.id}", json=payload, timeout=10)
    print(json.dumps(r.json(), indent=2))
    r.raise_for_status()


def delete(args):
    r = requests.delete(f"{API}/products/{args.id}", timeout=10)
    print(r.status_code)


def main():
    parser = argparse.ArgumentParser(description="Minimal CLI client for Product API")
    sub = parser.add_subparsers(required=True)

    pcreate = sub.add_parser("create")
    pcreate.add_argument("--name", required=True)
    pcreate.add_argument("--qty", type=int, required=True)
    pcreate.add_argument("--price", type=float, required=True)
    pcreate.set_defaults(func=create)

    plist = sub.add_parser("list")
    plist.set_defaults(func=list_)

    pget = sub.add_parser("get")
    pget.add_argument("id", type=int)
    pget.set_defaults(func=get_)

    pupd = sub.add_parser("update")
    pupd.add_argument("id", type=int)
    pupd.add_argument("--name")
    pupd.add_argument("--qty", type=int)
    pupd.add_argument("--price", type=float)
    pupd.set_defaults(func=update)

    pdel = sub.add_parser("delete")
    pdel.add_argument("id", type=int)
    pdel.set_defaults(func=delete)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
