# Can I get a free AWS account for this purpose?

Yes. You can use the **AWS Free Tier** to build and test this safely.

**The Strategy**: You don't need to *spend* money to find waste; you just need to create a "dummy" resource that *looks* like waste to your script.

## 1. The Free Tier Limits (The Safety Zone)

AWS gives you **30GB of EBS Storage per month** for free (for the first 12 months).

* **The Trick**: As long as your total storage (running instances + detached volumes) is under 30GB, you pay \$0.
* **The Setup**: Create a tiny 1GB volume and detach it. Your script will see it as "waste," but AWS won't charge you because you are under the 30GB limit.

## 2. How to Create "Fake Waste" for Testing

Run these commands in your terminal (using the AWS CLI) to create the perfect test case for your script:

```bash
# 1. Create a tiny 1GB volume (Cost: Included in Free Tier)
aws ec2 create-volume \
    --availability-zone us-east-1a \
    --size 1 \
    --volume-type gp3

# Output will give you a VolumeId (e.g., vol-1234567890abcdef0)
```

**That's it.** You now have a "Detached Volume."

* It is **Available** (not In-use).
* It is **1GB** (Tiny).
* Your script should find it and say: *"Found 1 detached volume. Wasting \$0.08/month."*

## 3. Verification

Once your script finds it and deletes it (via the `--confirm` flag), run this to prove it's gone:

```bash
aws ec2 describe-volumes --volume-ids vol-1234567890abcdef0
```

It should return an error: `InvalidVolume.NotFound`.

**Proceed.** You have everything you need to build the MVP without spending a cent.
