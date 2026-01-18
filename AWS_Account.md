<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Can I get a free AWS account for this purpose?

Yes. You can use the **AWS Free Tier** to build and test this safely.

**The Strategy**: You don't need to *spend* money to find waste; you just need to create a "dummy" resource that *looks* like waste to your script.

### 1. The Free Tier Limits (The Safety Zone)

AWS gives you **30GB of EBS Storage per month** for free (for the first 12 months).

* **The Trick**: As long as your total storage (running instances + detached volumes) is under 30GB, you pay \$0.
* **The Setup**: Create a tiny 1GB volume and detach it. Your script will see it as "waste," but AWS won't charge you because you are under the 30GB limit.


### 2. How to Create "Fake Waste" for Testing

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


### 3. Verification

Once your script finds it and deletes it (via the `--confirm` flag), run this to prove it's gone:

```bash
aws ec2 describe-volumes --volume-ids vol-1234567890abcdef0
```

It should return an error: `InvalidVolume.NotFound`.

**Proceed.** You have everything you need to build the MVP without spending a cent.
<span style="display:none">[^1][^10][^11][^12][^13][^14][^15][^2][^3][^4][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://aws.amazon.com/ebs/pricing/

[^2]: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-free-tier-usage.html

[^3]: https://www.reddit.com/r/aws/comments/1jfysan/ebs_free_tier_30gb_any_peak_storage_limit/

[^4]: https://www.reddit.com/r/aws/comments/10kclt7/cant_figure_why_i_extend_ebs_free_tier_limit/

[^5]: https://www.cloudoptimo.com/blog/aws-free-tier-isnt-unlimited-know-the-limits-before-you-get-billed/

[^6]: https://cloudfix.com/blog/reduce-aws-costs-deleting-unnecessary-ebs-volumes/

[^7]: https://zesty.co/blog/guide-to-ebs-pricing/

[^8]: https://www.reddit.com/r/aws/comments/v9ot0o/question_about_ebs_30gb_free_tier/

[^9]: https://docs.aws.amazon.com/ebs/latest/userguide/ebs-detaching-volume.html

[^10]: https://www.nops.io/blog/how-much-does-aws-ebs-storage-cost/

[^11]: https://www.cloudbolt.io/guide-to-aws-cost-optimization/aws-ebs-pricing/

[^12]: https://www.reddit.com/r/aws/comments/14901iy/ebs_free_tier_replace_root/

[^13]: https://www.reddit.com/r/aws/comments/ijozj4/pricing_5tb_of_unused_ebs_volume/

[^14]: https://www.reddit.com/r/aws/comments/aiyd5z/free_tier_noob_question/

[^15]: https://docs.aws.amazon.com/managedservices/latest/ctref/management-advanced-ebs-volume-detach.html

