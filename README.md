# AutoInsuranceUnderwritingManualGenAI
### The full example of the Step Function worked through is in the AutoUnderwritingProcess-Example folder.

The user begins by uploading a picture of their driver's license. The individual's first name, last name, and driver's license number are extracted to retrieve their driving history. Once the driving history is obtained, Amazon Bedrock, along with the LLM, uses the UnderwritingAutoInsuranceManual document to decide whether the user should be granted auto insurance. Currently, the Lambda function (dmv_api_call.py) retrieves information from an Excel sheet it is linked to. However, once connected to the DMV API, this model will work seamlessly.


Architecture Diagram:

<img width="406" alt="image" src="https://github.com/user-attachments/assets/455e6a29-af96-41b2-8abf-c266723c60ac">

Purpose: To streamline the insurance underwriting process with generative AI, automating data extraction, delivering real-time insights for underwriters.

Responsible AI: Ensuring fairness, transparency, and security to deliver unbiased, and secure insurance underwriting decisions that comply with ethical standards and protect sensitive data.

Key Features:
Data Privacy: Metadata filtering ensures secure access to sensitive insurance data.

Generative AI: Amazon Bedrock automates underwriting by extracting insights from large data sets.

Business Rules: AI models are aligned with underwriting guidelines for consistent decision-making.

Real-Time Processing: Scalable infrastructure handles high volumes of documents efficiently.

Fair Underwriting: The solution excludes irrelevant factors like marital status to promote fairness.

