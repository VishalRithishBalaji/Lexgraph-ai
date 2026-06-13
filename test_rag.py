from my_project.rag import ingest_pdf, retrieve_context

ingest_pdf("uploads/test.pdf")

print("\n===== QUERY 1 =====")
print(retrieve_context("What evidence exists?"))

print("\n===== QUERY 2 =====")
print(retrieve_context("Who are the witnesses?"))

print("\n===== QUERY 3 =====")
print(retrieve_context("What financial evidence is mentioned?"))