from pepper import app, config, logger


def cli():
    logger.info("Start CLI process")
    # q1 = QueueManager("shipment_updates")
    # q1.push({"shipment_id": 1, "status": "in_transit"})
    # q1.push({"shipment_id": 2, "status": "delivered"})
    # print(q1.pop())
    # print(q1.pop())
    # print(q1.size())  # → 0
    # print(QueueManager.list_queues())

    # users = CachedDictList("users", index_keys=["id", "email"])
    # users.add({"id": 1, "email": "a@example.com", "name": "Alice"})
    # users.add({"id": 2, "email": "b@example.com", "name": "Bob"})
    # matches = users.filter_by_key("email", "a@example.com")
    # print(matches)
    # bobs = users.find(lambda d: d["name"].startswith("B"))
    # print(bobs)
    #
    # def updater(d):
    #     d["name"] = d["name"].upper()
    #     return d
    #
    # count = users.update(lambda x: x["id"] == 2, updater)
    # print("updated", count)
    # removed = users.remove(lambda d: d["id"] == 1)
    # print("removed", removed)
    # all_items = users.get_all()
    # print(all_items)


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1")
