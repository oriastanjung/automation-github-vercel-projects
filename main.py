from src.core.automatic_deployment import automatic_deployment
import asyncio

async def main():
    deployment_vercel_url, hosted_vercel_url, is_error = await automatic_deployment(
        json_file_path="sample.json", uuid="userId", repo_name="project-4"
    )
    print("deployment_vercel_url", deployment_vercel_url)
    print("hosted_vercel_url", hosted_vercel_url)
    print("is_error", is_error)

if __name__ == "__main__":
    asyncio.run(main())