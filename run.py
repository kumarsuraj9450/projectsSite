import uvicorn

if __name__ == "__main__":
	def acc_camvid(input, target):
	    target = target.squeeze(1)
	    mask = target != void_code
	    return (input.argmax(dim=1)[mask]==target[mask]).float().mean()
	    
	uvicorn.run("project:app", host = "127.0.0.1", port = 8000, workers = 1)